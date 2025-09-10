from pifmpsrt.utils import pad_to_8, center_to_8

def generate_ps_frames(mode, text, times=None):
    frames = []

    if mode == "rs":  # справа налево
        ext = text + "_" * 7
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "ls":  # слева направо
        ext = text + "_" * 7
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "cs":  # появление из центра (просто пример)
        padded = center_to_8(text)
        for i in range(len(padded)):
            frames.append(pad_to_8(padded[i:i+8]))

    elif mode == "cst":  # центральный перенос
        ext = center_to_8(text) + "_" * 8
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "ss":  # циклический скролл
        ext = text + text[:7]
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    else:  # без режима → показать как есть
        frames.append(pad_to_8(text))

    return frames
