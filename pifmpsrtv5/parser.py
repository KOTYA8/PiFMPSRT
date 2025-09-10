def parse_line(line: str):
    """
    Пример строки: s|thisistexthello|5/4
    Возвращает: mode, text, times
    """
    parts = line.split("|")
    if len(parts) == 3:
        mode, text, times = parts
        times = [int(x) for x in times.split("/")]
    elif len(parts) == 2:
        mode, text = parts
        times = [5]  # по умолчанию 5 секунд
    else:
        raise ValueError(f"Неправильный формат строки: {line}")
    return mode, text, times
