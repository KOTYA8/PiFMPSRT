import os
from .utils import align_ps


def parse_ps_line(raw_line: str):
    line = raw_line.rstrip("\n")
    if not line or line.lstrip().startswith("#"):
        return None

    # задержки
    delay_list = [5]
    core = line
    pos_last = line.rfind("|")
    if pos_last != -1:
        tail = line[pos_last + 1:]
        if "/" in tail:
            try:
                delay_list = [int(x) for x in tail.strip().split("/") if x]
                core = line[:pos_last]
            except ValueError:
                core = line
        else:
            try:
                delay_list = [int(tail.strip())]
                core = line[:pos_last]
            except ValueError:
                core = line

    # режим
    mode_token = ""
    text = core
    first_bar = core.find("|")
    if first_bar != -1:
        mode_token = core[:first_bar]
        text = core[first_bar + 1:]

    kind = "normal"
    align = "l"
    n = 8
    scroll_mode = None

    mt = mode_token

    if mt in ("s", "ls", "cs", "cts", "rs", "ss"):
        kind = "scroll"
        scroll_mode = mt
    elif mt.startswith(("l", "c", "r")):
        align = mt[0]
        rest = mt[1:]
        if rest.startswith("t"):
            kind = "transfer"
            try:
                n_val = int(rest[1:])
                if 1 <= n_val <= 8:
                    n = n_val
            except ValueError:
                n = 8
    elif mt.startswith("t"):
        kind = "transfer"
        try:
            n_val = int(mt[1:])
            if 1 <= n_val <= 8:
                n = n_val
        except ValueError:
            n = 8

    return {
        "kind": kind,
        "align": align,
        "n": n,
        "text": text,
        "delays": delay_list,
        "scroll_mode": scroll_mode,
    }


def ps_frames(entry):
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delays = entry["delays"]
    scroll_mode = entry.get("scroll_mode", None)

    delay_count = len(delays)
    idx = 0

    if kind == "normal":
        yield align_ps(text, align), delays[0]

    elif kind == "transfer":
        if n <= 0:
            n = 8
        for i in range(0, len(text), n):
            seg = text[i:i+n]
            d = delays[idx % delay_count]
            idx += 1
            yield align_ps(seg, align), d

    elif kind == "scroll":
        pad_text = text
        if scroll_mode in ("cs", "cst") and len(pad_text) < 8:
            pad_text = pad_text.ljust(8)

        if scroll_mode in ("s", "rs"):  # обычный справа-налево
            for i in range(0, len(text) - 7):
                d = delays[idx % delay_count]
                idx += 1
                yield text[i:i+8], d

        elif scroll_mode == "ls":  # слева-направо
            pad = "_" * 7 + text
            for i in range(len(text)):
                d = delays[idx % delay_count]
                idx += 1
                yield pad[i:i+8], d

        elif scroll_mode == "ss":  # циклический
            cycle = text + text[:7]
            for i in range(len(text) + 7):
                d = delays[idx % delay_count]
                idx += 1
                yield cycle[i:i+8], d

        elif scroll_mode == "cs":  # центр. искажение
            for i in range(len(pad_text)):
                corrupted = list(pad_text.ljust(8))
                if i < 8:
                    corrupted[i] = "x"
                frame = "".join(corrupted[:8])
                d = delays[idx % delay_count]
                idx += 1
                yield frame, d

        elif scroll_mode == "cts":  # центр. перенос
            for i in range(len(pad_text)):
                corrupted = list(pad_text.ljust(8))
                corrupted[i % 8] = "_"
                frame = "".join(corrupted[:8])
                d = delays[idx % delay_count]
                idx += 1
                yield frame, d


def load_ps_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]
