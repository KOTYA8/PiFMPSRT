from utils import pad_to_8, center_to_8

def generate_ps_frames(mode, text, times=None):
    frames = []

    if mode == "rs":  # обычный скролл (справа налево)
        ext = text + "_" * 7
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "ls":  # левый скролл
        ext = "_" * 7 + text
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "cs":  # появление из центра
        padded = center_to_8(text)
        for i in range(len(padded)):
            frames.append(pad_to_8(padded[i:i+8]))

    elif mode == "cst":  # центральный перенос (постепенный выход)
        ext = center_to_8(text) + "_" * 8
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    elif mode == "ss":  # циклический скролл
        ext = text + text[:7]
        for i in range(len(ext) - 7):
            frames.append(pad_to_8(ext[i:i+8]))

    else:  # просто показать как есть
        frames.append(pad_to_8(text))

    return frames
