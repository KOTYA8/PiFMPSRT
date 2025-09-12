# ps_parser.py
# Парсер режимов для RDS PS

def generate_ps_frames(mode: str, text: str):
    """
    Генерирует список кадров PS для разных режимов:
    ps| - статичный текст (8 символов)
    ts| - бегущая строка
    t1-t7| - тестовые варианты
    cs| - центрированный скролл
    """

    frames = []

    # Унифицированная подготовка текста
    text = str(text)
    if mode == "ps":
        # Статичный PS (ровно 8 символов)
        ps = text.ljust(8)[:8]
        frames.append(ps)

    elif mode == "ts":
        # Бегущая строка
        buf = text + "        "  # добавляем пробелы
        for i in range(len(buf) - 7):
            frames.append(buf[i:i+8])

    elif mode.startswith("t") and len(mode) == 2 and mode[1].isdigit():
        # Тестовые режимы t1…t7
        num = int(mode[1])
        ps = (text + " " * 8)[:8]
        for i in range(num):
            shifted = ps[i:] + ps[:i]
            frames.append(shifted)

    elif mode == "cs":
        # Центрированный скролл
        buf = text + " " * 8  # запас пробелов для окончания
        window = list(buf[:8])  # стартовое окно

        frames.append("".join(window))  # первая рамка

        idx = 8  # указывает на следующий символ из текста
        step = 0
        while idx < len(buf):
            step += 1
            if step == 1:
                # заменяем 4-й символ
                window[3] = buf[idx]
            elif step == 2:
                # заменяем 5-й символ
                window[4] = buf[idx]
            elif step == 3:
                # сдвиг 3–4 символов влево + вставка
                window[2:5] = window[3:6]
                window[4] = buf[idx]
            elif step == 4:
                # вставка на 6-ю позицию
                window[5] = buf[idx]
            elif step == 5:
                # сдвиг 3–6 символов влево + вставка
                window[2:6] = window[3:7]
                window[5] = buf[idx]
            elif step == 6:
                # вставка на 7-ю позицию
                window[6] = buf[idx]
            elif step == 7:
                # сдвиг 2–7 символов влево + вставка
                window[1:7] = window[2:8]
                window[6] = buf[idx]
                step = 0  # сброс цикла
            else:
                step = 0
                continue

            frames.append("".join(window))
            idx += 1

        # Дополняем последнюю рамку пробелами
        frames.append("".join(window).ljust(8))

    else:
        raise ValueError(f"Неизвестный режим: {mode}")

    return frames


if __name__ == "__main__":
    # Примеры проверки
    print("PS:", generate_ps_frames("ps", "HELLO123"))
    print("TS:", generate_ps_frames("ts", "HELLO123"))
    print("T3:", generate_ps_frames("t3", "HELLO123"))
    print("CS:", generate_ps_frames("cs", "thisistexthello"))
