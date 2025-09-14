import os
import time

def load_file_text(file_path):
    """Считываем текст из file.txt"""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def parse_file_line(line, file_path):
    """
    Разбираем строку с f, fb, fe, rfe, cf, cfe, lsf, sf, tf
    line: строка из ps.txt или rt.txt
    file_path: путь к file.txt
    """
    entry = {"mode": None, "text": "", "delays": [5], "align": "l", "n": 8}

    if not line or line.lstrip().startswith("#"):
        return None

    parts = line.split("|")
    mode = parts[0]
    entry["mode"] = mode

    # Последняя часть может содержать задержки
    if len(parts) > 1:
        tail = parts[-1]
        delays = []
        for x in tail.replace("\\","/").split("/"):
            try:
                delays.append(int(x))
            except ValueError:
                continue
        if delays:
            entry["delays"] = delays

    # Основной текст из файла
    file_text = load_file_text(file_path)

    # Текст до и после (fb, fe)
    start_text = ""
    end_text = ""
    for p in parts[1:-1]:
        if p.startswith("fb"):
            start_text = p[2:]
        elif p.startswith("fe"):
            end_text = p[2:]

    entry["text"] = f"{start_text}{file_text}{end_text}"

    # Выравнивание
    if mode.startswith("l"):
        entry["align"] = "l"
    elif mode.startswith("c"):
        entry["align"] = "c"
    elif mode.startswith("r"):
        entry["align"] = "r"
    else:
        entry["align"] = "l"

    # n для transfer
    if "t" in mode:
        try:
            n_val = int("".join(filter(str.isdigit, mode)))
            if 1 <= n_val <= 8:
                entry["n"] = n_val
        except:
            entry["n"] = 8

    return entry

def watch_file_for_change(file_path, last_text):
    """
    Проверка изменения текста в файле.
    Возвращает: (changed: bool, current_text: str)
    """
    current_text = load_file_text(file_path)
    changed = current_text != last_text
    return changed, current_text
