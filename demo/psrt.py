import time
import subprocess
from threading import Thread
from pifmpsrt.ps_parser import ps_frames  # старый рабочий модуль
from pifmpsrt.file_parser import parse_file_line, watch_file_for_change, load_file_text

RDS_CTL = "rds_ctl"

PS_FILE = "pifmpsrt/ps.txt"
RT_FILE = "pifmpsrt/rt.txt"
FILE_TXT = "pifmpsrt/file.txt"

last_file_text = ""
ps_entries = []
rt_entries = []

def load_entries(file_path):
    """Загрузить команды из ps.txt или rt.txt"""
    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Если команда с файлом
            if any(line.startswith(x) for x in ["f", "fb", "fe", "lsf", "sf", "tf", "cf", "cfe", "rfe"]):
                entry = parse_file_line(line, FILE_TXT)
            else:
                entry = parse_file_line(line, None)  # обычная PS/RT команда
            if entry:
                entries.append(entry)
    return entries

def run_ps_cycle():
    global last_file_text, ps_entries
    ps_entries = load_entries(PS_FILE)
    last_file_text = load_file_text(FILE_TXT)

    while True:
        # Проверка изменения file.txt
        changed, current_text = watch_file_for_change(FILE_TXT, last_file_text)
        if changed:
            last_file_text = current_text
            for i, entry in enumerate(ps_entries):
                if entry["mode"].startswith(("f","fb","fe","lsf","sf","tf","cf","cfe","rfe")):
                    # Обновляем текст из файла
                    ps_entries[i] = parse_file_line(entry["mode"]+"|"+entry["text"], FILE_TXT)

        for entry in ps_entries:
            for frame, delay in ps_frames(entry):
                subprocess.run([RDS_CTL, "PS", frame])
                time.sleep(delay)

def run_rt_cycle():
    global last_file_text, rt_entries
    rt_entries = load_entries(RT_FILE)
    last_file_text = load_file_text(FILE_TXT)

    while True:
        changed, current_text = watch_file_for_change(FILE_TXT, last_file_text)
        if changed:
            last_file_text = current_text
            for i, entry in enumerate(rt_entries):
                if entry["mode"].startswith(("f","fb","fe","lsf","sf","tf","cf","cfe","rfe")):
                    rt_entries[i] = parse_file_line(entry["mode"]+"|"+entry["text"], FILE_TXT)

        for entry in rt_entries:
            for frame, delay in ps_frames(entry):
                subprocess.run([RDS_CTL, "RT", frame])
                time.sleep(delay)

if __name__ == "__main__":
    t1 = Thread(target=run_ps_cycle, daemon=True)
    t2 = Thread(target=run_rt_cycle, daemon=True)
    t1.start()
    t2.start()
    while True:
        time.sleep(1)
