from utils import pad_to_8

def generate_transfer_frames(mode, text):
    frames = []

    # Обычный перенос (t)
    if mode == "t":
        step = 8
        for i in range(0, len(text), step-1):
            frames.append(pad_to_8(text[i:i+step]))

    # Показание 2 символов (t2)
    elif mode == "t2":
        step = 2
        for i in range(0, len(text), step):
            frames.append(pad_to_8(text[i:i+step]))

    # Показание 4 символов (t4)
    elif mode == "t4":
        step = 4
        for i in range(0, len(text), step):
            frames.append(pad_to_8(text[i:i+step]))

    # Показание 6 символов (t6)
    elif mode == "t6":
        step = 6
        for i in range(0, len(text), step):
            frames.append(pad_to_8(text[i:i+step]))

    return frames
