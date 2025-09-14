# pifmpsrt/ps_parser.py

from .ps_scroll import scroll_ps
from .ps_line_split import line_split_ps
from .file_watcher import FileWatcher

# Словарь с последними значениями файлов (для fb/fe/cf и т.д.)
file_watchers = {
    "file.txt": FileWatcher("file.txt"),
    "ps.txt": FileWatcher("ps.txt"),
    "rt.txt": FileWatcher("rt.txt"),
}

def handle_file_module(parts):
    """
    Обработка модулей, связанных с файлами (f|, fb|, fe|, cf|, rfe| и т.д.)
    """
    cmd = parts[0]  # например "f", "fb", "fe", "cf", "rfe"

    # Основной текст из файла
    file_text = file_watchers["file.txt"].get_text()

    # fb| → текст добавляется в начале
    if cmd.startswith("fb"):
        prefix = parts[1] if len(parts) > 1 else ""
        return prefix + file_text

    # fe| → текст добавляется в конце
    if cmd.startswith("fe"):
        suffix = parts[1] if len(parts) > 1 else ""
        return file_text + suffix

    # fb|...|e|... (и середина, и конец)
    if cmd.startswith("fb") and "e" in parts:
        prefix = parts[1] if len(parts) > 1 else ""
        suffix = parts[3] if len(parts) > 3 else ""
        return prefix + file_text + suffix

    # cf| → выравнивание по центру
    if cmd.startswith("cf"):
        return file_text.center(8)

    # rfe| → справа + суффикс
    if cmd.startswith("rfe"):
        suffix = parts[1] if len(parts) > 1 else ""
        return (file_text + suffix).rjust(8)

    # f| → просто содержимое файла
    if cmd.startswith("f"):
        return file_text

    # По умолчанию вернём как есть
    return file_text


def parse_ps_line(line: str):
    """
    Основной парсер строк PS
    """
    line = line.strip()

    # Если строка пустая
    if not line:
        return ""

    # Если строка не содержит командных символов | → обычный текст
    if "|" not in line and not line.startswith(("s", "lt", "tf", "sf", "f", "cf", "fb", "fe", "rfe", "lsf")):
        return line

    # Если строка начинается с | → это обычный текст
    if line.startswith("|"):
        return line[1:]

    parts = line.split("|")

    # SCROLL (s|TEXT|SPEED)
    if parts[0] == "s":
        text = parts[1] if len(parts) > 1 else ""
        try:
            speed = int(parts[2]) if len(parts) > 2 else 3
        except ValueError:
            speed = 3
        return scroll_ps(text, speed)

    # LINE SPLIT (ltN|TEXT)
    if parts[0].startswith("lt"):
        try:
            width = int(parts[0][2:])
        except ValueError:
            width = 8
        text = parts[1] if len(parts) > 1 else ""
        return line_split_ps(text, width)

    # FILE MODULES (f|, fb|, fe|, cf|, rfe|, lsf| и т.д.)
    if parts[0].startswith(("f", "cf", "fb", "fe", "rfe", "sf", "tf", "lsf", "lt")):
        return handle_file_module(parts)

    # Всё остальное → просто текст
    return line
