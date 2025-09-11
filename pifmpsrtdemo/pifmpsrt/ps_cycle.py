import os, time
from .ps_parser import parse_ps_line, ps_frames
from .utils import send_cmd

def load_ps_list(filename):
    if not os.path.exists(filename):
        return []
    items = []
    with open(filename, "r", encoding="utf-8") as fh:
        for line in fh:
            e = parse_ps_line(line)
            if e:
                items.append(e)
    return items

def cycle_ps(ps_file, fifo):
    while True:
        ps_list = load_ps_list(ps_file)
        if not ps_list:
            time.sleep(1)
            continue
        for entry in ps_list:
            for frame, delay in ps_frames(entry):
                send_cmd(fifo, f"PS {frame}")
                time.sleep(delay)
