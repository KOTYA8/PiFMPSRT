import os, time
from .utils import send_cmd

def align_rt(txt: str, align: str) -> str:
    """Выравнивание RT текста в 64 символах"""
    if len(txt) > 64:
        txt = txt[:64]
    pad = 64 - len(txt)
    if align == "r":
        return " " * pad + txt
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + txt + " " * right
    return txt + " " * pad

def load_rt_list(filename):
    if not os.path.exists(filename):
        return []
    items = []
    with open(filename, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            align = "l"
            core = line
            if line.startswith(("l|", "c|", "r|")):
                align = line[0]
                core = line[2:]

            delay = 5
            k = core.rfind("|")
            if k != -1:
                tail = core[k+1:]
                try:
                    delay = int(tail.strip())
                    core = core[:k]
                except ValueError:
                    pass
            items.append((core, delay, align))
    return items

def cycle_rt(rt_file, fifo):
    while True:
        rt_list = load_rt_list(rt_file)
        if not rt_list:
            time.sleep(1)
            continue
        for rt, d, align in rt_list:
            txt = align_rt(rt, align)
            send_cmd(fifo, f"RT {txt}")
            time.sleep(d)
