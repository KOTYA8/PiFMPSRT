import re
from itertools import cycle
from file_watcher import FileWatcher

file_watcher = FileWatcher("file.txt")

def align_ps(text, align="l"):
    if len(text) >= 8:
        return text[:8]
    pad = 8 - len(text)
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + text + " " * right
    elif align == "r":
        return " " * pad + text
    else:
        return text + " " * pad

def parse_ps_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    m = re.match(r"([lcr]?)([a-z0-9]+)?f?b?(?:\|([^|]*))?(?:e\|([^|]*))?\|(.+)?", line)
    if not m:
        return None

    align, mode, prefix, suffix, rest = m.groups()
    align = align or "l"
    mode = mode or "normal"

    # ищем секунды и expire
    sec_match = re.search(r"\|([\d/]+)(?:\\(\d+))?$", line)
    delays, expire_time = [5], None
    if sec_match:
        sec_str, expire_str = sec_match.groups()
        if sec_str:
            delays = [int(x) for x in sec_str.split("/")]
        if expire_str:
            expire_time = int(expire_str)

    # проверка на file
    if "f" in mode:
        kind = "file"
    elif mode == "s":
        kind = "scroll"
    elif mode == "ss":
        kind = "scroll_cycle"
    elif mode == "t":
        kind = "transfer"
    elif mode.startswith("t") and mode[1:].isdigit():
        kind = "transfer_cut"
    elif mode == "ls":
        kind = "scroll_lr"
    else:
        kind = "normal"

    return {
        "kind": kind,
        "align": align,
        "delays": delays,
        "expire_time": expire_time,
        "prefix": prefix or "",
        "suffix": suffix or "",
        "text": rest or "",
    }

def ps_frames(entry):
    kind = entry["kind"]
    text = entry["text"]
    delays = entry["delays"]
    delay_count = len(delays)
    align = entry["align"]
    prefix = entry["prefix"]
    suffix = entry["suffix"]
    expire_time = entry["expire_time"]

    if kind == "file":
        file_text = file_watcher.read()
        if not file_text or (expire_time and not file_watcher.changed_recently(expire_time)):
            return
        final_text = prefix + file_text + suffix
        yield align_ps(final_text, align), delays[0]

    elif kind == "normal":
        yield align_ps(text, align), delays[0]

    elif kind == "scroll":
        if len(text) <= 8:
            yield align_ps(text, align), delays[0]
        else:
            for i in range(len(text) - 7):
                yield text[i:i+8], delays[i % delay_count]

    elif kind == "scroll_cycle":
        idx = 0
        length = len(text)
        while True:
            window = "".join(text[(idx + j) % length] for j in range(8))
            yield window, delays[idx % delay_count]
            idx += 1

    elif kind == "transfer":
        if len(text) <= 8:
            yield align_ps(text, align), delays[0]
        else:
            step = 8
            parts = [text[i:i+step] for i in range(0, len(text), step)]
            for i, p in enumerate(parts):
                yield align_ps(p, align), delays[i % delay_count]

    elif kind == "transfer_cut":
        cut = int(entry["kind"][1:])
        if len(text) <= 8:
            yield align_ps(text, align), delays[0]
        else:
            step = 8 - (cut // 2)
            parts = [text[i:i+step] for i in range(0, len(text), step)]
            for i, p in enumerate(parts):
                yield align_ps(p, align), delays[len(p) % delay_count]

    elif kind == "scroll_lr":
        if len(text) <= 8:
            yield align_ps(text, "l"), delays[0]
        else:
            base = text[:8]
            yield base, delays[0]
            idx = 1
            for k in range(len(text) - 1, -1, -1):
                sym = text[k]
                base = sym + base[:-1]
                d = delays[idx % delay_count]
                idx += 1
                yield base, d
