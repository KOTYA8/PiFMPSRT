import os

def send_cmd(fifo, cmd: str):
    """Отправка команды в rds_ctl (FIFO)."""
    if not os.path.exists(fifo):
        print(f"[WARN] FIFO {fifo} не найден")
        return
    with open(fifo, "w") as f:
        f.write(cmd + "\n")

def align_ps(txt: str, align: str) -> str:
    """Выравнивание текста PS (8 символов)."""
    if len(txt) > 8:
        txt = txt[:8]
    pad = 8 - len(txt)
    if align == "r":
        return " " * pad + txt
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + txt + " " * right
    return txt + " " * pad
