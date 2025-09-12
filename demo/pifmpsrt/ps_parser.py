import re
from .ps_scroll import scroll_ls, scroll_rs, scroll_ss, scroll_cs, scroll_cts

def parse_ps_line(line):
    """
    Разбор строки ps.txt
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = line.split("|")
    if len(parts) < 2:
        return None

    mt = parts[0]  # режим (например t4, s, ls, rs, cs, cts)
    text = parts[1]
    delays = [int(x) for x in parts[2].split("/")] if len(parts) > 2 else [5]

    align = "l"
    kind = "normal"
    n = 8

    if mt.startswith(("l", "c", "r")):
        align = mt[0]
        rest = mt[1:]
        if rest == "" or rest is None:
            kind = "normal"
        elif rest.startswith("t"):
            kind = "transfer"
            if len(rest) == 1:
                n = 8
            else:
                try:
                    n_val = int(rest[1:])
                    if 1 <= n_val <= 8:
                        n = n_val
                except ValueError:
                    n = 8
    elif mt.startswith("t"):
        kind = "transfer"
        if len(mt) == 1:
            n = 8
        else:
            try:
                n_val = int(mt[1:])
                if 1 <= n_val <= 8:
                    n = n_val
            except ValueError:
                n = 8
    elif mt.startswith("s"):
        kind = "scroll"
    elif mt in ["ls", "rs", "ss", "cs", "cts"]:
        kind = mt
    else:
        kind = "normal"

    return {
        "kind": kind,
        "align": align,
        "n": n,
        "text": text,
        "delays": delays,
    }


def align_ps(text, align):
    if len(text) > 8:
        text = text[:8]
    if align == "l":
        return text.ljust(8)
    elif align == "c":
        return text.center(8)
    elif align == "r":
        return text.rjust(8)
    return text.ljust(8)


def ps_frames(entry):
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delays = entry["delays"]

    delay_count = len(delays)
    idx = 0

    if kind == "normal":
        yield align_ps(text, align), delays[0]

    elif kind == "scroll":
        pad = text + " " * 7
        while True:
            for i in range(len(pad) - 7):
                yield pad[i:i+8], delays[idx % delay_count]
                idx += 1

    elif kind == "transfer":
        chunks = []
        for i in range(0, len(text), n):
            chunk = text[i:i+n]
            chunks.append(chunk.ljust(8))
        if not chunks:
            chunks = [" " * 8]
        while True:
            for chunk in chunks:
                yield chunk, delays[idx % delay_count]
                idx += 1

    elif kind in ["ls", "rs", "ss", "cs", "cts"]:
        if kind == "ls":
            gen = scroll_ls(text)
        elif kind == "rs":
            gen = scroll_rs(text)
        elif kind == "ss":
            gen = scroll_ss(text)
        elif kind == "cs":
            gen = scroll_cs(text)
        elif kind == "cts":
            gen = scroll_cts(text)

        while True:
            frame = next(gen)
            yield frame.ljust(8), delays[idx % delay_count]
            idx += 1
