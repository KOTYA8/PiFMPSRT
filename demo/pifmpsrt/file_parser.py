import os
import time

def load_file_text(file_path):
    """Считываем текст из файла file.txt"""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def parse_file_line(line, file_path):
    """Разбираем строку с f, fb, fe, rfe, cf и т.д."""
    entry = {"mode": None, "text": "", "delays": [5], "align": "l", "n": 8}

    if not line or line.lstrip().startswith("#"):
        return None

    # Разделяем по |
    parts = line.split("|")
    mode = parts[0]
    entry["mode"] = mode

    # Секунды через \ или /
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

    # Базовый текст из файла
    file_text = load_file_text(file_path)

    # Определяем позицию и комбинацию текста
    custom_text = ""
    start_text = ""
    end_text = ""
    for p in parts[1:-1]:
        if p.startswith("fb"):
            start_text = p[2:]
        elif p.startswith("fe"):
            end_text = p[2:]
        else:
            custom_text = p

    entry["text"] = f"{start_text}{file_text}{end_text}"

    # Определяем выравнивание
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
            n = int(mode[1:])
            if 1 <= n <= 8:
                entry["n"] = n
        except:
            entry["n"] = 8

    return entry
