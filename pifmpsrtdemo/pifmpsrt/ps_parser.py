def parse_delays(raw_tail: str):
    """Разбор времени задержек, например 5/4/6 → [5,4,6]."""
    parts = raw_tail.split("/")
    delays = []
    for p in parts:
        try:
            delays.append(int(p.strip()))
        except ValueError:
            continue
    return delays if delays else [5]

def parse_ps_line(raw_line: str):
    """Парсинг строки из ps.txt"""
    line = raw_line.rstrip("\n")
    if not line or line.lstrip().startswith("#"):
        return None

    core = line
    delays = [5]

    pos_last = line.rfind("|")
    if pos_last != -1:
        tail = line[pos_last + 1:]
        d = parse_delays(tail)
        if d:
            delays = d
            core = line[:pos_last]

    mode_token = ""
    text = core
    first_bar = core.find("|")
    if first_bar != -1:
        mode_token = core[:first_bar]
        text = core[first_bar + 1:]

    kind = "normal"
    align = "l"
    n = 8
    mt = mode_token

    if mt == "s":
        kind = "scroll"
    else:
        if mt.startswith(("l", "c", "r")):
            align = mt[0]
            rest = mt[1:]
            if rest == "" or rest is None:
                kind = "normal"
            elif rest.startswith("t"):
                kind = "transfer"
                try:
                    n = int(rest[1:]) if len(rest) > 1 else 8
                except ValueError:
                    n = 8
        elif mt.startswith("t"):
            kind = "transfer"
            try:
                n = int(mt[1:]) if len(mt) > 1 else 8
            except ValueError:
                n = 8
            align = "l"

    return {"kind": kind, "align": align, "n": n, "text": text, "delays": delays}

def ps_frames(entry):
    """Генерация кадров для PS"""
    from .utils import align_ps
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delays = entry["delays"]

    if kind == "normal":
        yield (align_ps(text, align), delays[0])
    elif kind == "scroll":
        if len(text) <= 8:
            yield (align_ps(text, "l"), delays[0])
        else:
            idx = 0
            for i in range(0, len(text) - 7):
                yield (text[i:i+8], delays[idx % len(delays)])
                idx += 1
    elif kind == "transfer":
        if n <= 0:
            n = 8
        idx = 0
        for i in range(0, len(text), n):
            seg = text[i:i+n]
            yield (align_ps(seg, align), delays[idx % len(delays)])
            idx += 1
