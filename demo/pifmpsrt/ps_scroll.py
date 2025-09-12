def scroll_ls(text: str):
    """
    Left scroll (ls) — символы с конца текста переносятся вперед,
    всё циклично.
    """
    buf = list(text.ljust(8))  # гарантируем минимум 8 символов
    while True:
        yield "".join(buf[:8])
        # перенос последнего символа в начало
        ch = buf.pop(-1)
        buf.insert(0, ch)


def scroll_rs(text: str):
    """
    Right scroll (rs) — обычный скролл справа налево.
    """
    pad = text + " " * 7
    while True:
        for i in range(len(pad) - 7):
            yield pad[i:i+8]


def scroll_ss(text: str):
    """
    Cyclic scroll (ss) — полный круговой скролл по всему тексту.
    """
    buf = text
    while True:
        for i in range(len(buf)):
            win = (buf + buf)[i:i+8]
            yield win


def scroll_cs(text: str):
    """
    Center scroll (cs) — появление текста из середины.
    Работает с любым количеством символов.
    """
    buf = [" "] * 8
    chars = list(text)
    idx = 0
    while idx < len(chars):
        if idx < 8:
            buf[idx] = chars[idx]
        else:
            buf = buf[1:] + [" "]
            buf[-1] = chars[idx]
        yield "".join(buf)
        idx += 1
    for _ in range(8):
        buf = buf[1:] + [" "]
        yield "".join(buf)


def scroll_cts(text: str):
    """
    Center transfer scroll (cts).
    """
    buf = [" "] * 8
    chars = list(text)
    idx = 0
    while idx < len(chars):
        pos = idx % 8
        buf[pos] = chars[idx]
        yield "".join(buf)
        idx += 1
    for _ in range(8):
        buf[(idx % 8)] = " "
        idx += 1
        yield "".join(buf)
