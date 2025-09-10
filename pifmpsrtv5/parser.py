def parse_line(line: str):
    """
    Возможные форматы строк:
      text
      mode|text
      mode|text|5/4
    """
    if "|" not in line:
        return None, line, [5]  # просто текст
    
    parts = line.split("|")
    if len(parts) == 3:
        mode, text, times = parts
        times = [int(x) for x in times.split("/")]
    elif len(parts) == 2:
        mode, text = parts
        times = [5]
    else:
        raise ValueError(f"Неправильный формат строки: {line}")
    return mode, text, times
