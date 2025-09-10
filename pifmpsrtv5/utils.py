def pad_to_8(s: str) -> str:
    """Дополнить строку до 8 символов"""
    return s.ljust(8)[:8]

def center_to_8(s: str) -> str:
    """Центрирование текста в 8 символах"""
    return s.center(8)[:8]

def cycle_times(times, idx):
    """Выбор времени из списка с циклом"""
    if not times:
        return 5
    return times[idx % len(times)]
