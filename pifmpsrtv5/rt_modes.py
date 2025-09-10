from utils import pad_to_8, center_to_8

def generate_rt_frames(mode, text, times=None):
    if mode == "l":  # слева
        return [text]
    elif mode == "c":  # по центру
        return [center_to_8(text)]
    elif mode == "r":  # справа
        return [text.rjust(8)]
    else:
        return [text]
