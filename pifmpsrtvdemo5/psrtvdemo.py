#!/usr/bin/env python3
# psrt.py — PS/RT engine for PiFmRds (extended: times, scroll modes, transfer t2/t4/t6,...)
# Код использует FIFO rds_ctl (создаёт pi_fm_rds). Положите ps.txt и rt.txt рядом.

import os
import time
import threading
import itertools

RDS_CTL = "rds_ctl"   # fifo
ps_file = "ps.txt"
rt_file = "rt.txt"
DEFAULT_DELAYS = [5]

f = None
lock = threading.Lock()

# ---------- utilities ----------

def parse_delay_spec(spec: str):
    """"5" or "5/4/6" -> [5,4,6]"""
    if not spec:
        return DEFAULT_DELAYS[:]
    parts = spec.split("/")
    res = []
    for p in parts:
        try:
            v = int(p.strip())
            if v <= 0:
                continue
            res.append(v)
        except Exception:
            continue
    return res if res else DEFAULT_DELAYS[:]

def safe_open_fifo():
    """Открывает FIFO на запись, ожидая когда появится читатель."""
    global f
    # Если уже открыт и рабочий — вернуть
    try:
        if f:
            return f
    except NameError:
        pass
    # пытаемся открыть
    while True:
        try:
            f = open(RDS_CTL, "w")
            return f
        except FileNotFoundError:
            print(f"[WARN] FIFO {RDS_CTL} не найден. Убедитесь, что pi_fm_rds запущен в той же папке.")
            time.sleep(1)
        except BlockingIOError:
            time.sleep(0.5)
        except Exception as e:
            print(f"[WARN] ошибка при открытии FIFO: {e}")
            time.sleep(1)

def send_cmd(cmd: str):
    """Записывает команду в FIFO (и расшаривает ошибки)."""
    global f
    with lock:
        try:
            if not f:
                safe_open_fifo()
            f.write(cmd + "\n")
            f.flush()
        except BrokenPipeError:
            # Reader закрылся — попробуем переоткрыть
            try:
                f.close()
            except Exception:
                pass
            f = None
            print("[WARN] BrokenPipe, пытаюсь переоткрыть FIFO...")
            safe_open_fifo()
            try:
                f.write(cmd + "\n")
                f.flush()
            except Exception as e:
                print(f"[ERROR] не удалось отправить после reopen: {e}")
        except Exception as e:
            print(f"[ERROR] send_cmd: {e}")

# ---------- parsing PS lines ----------

SCROLL_MODES = {"s", "rs", "ls", "cs", "cst", "ss"}

def parse_ps_line(raw_line: str):
    """
    Поддерживаем формат:
      mode|TEXT|delay_spec
    где mode может быть:
      - (пусто) -> обычный left normal
      - l / c / r  -> alignment for normal
      - s (или rs) -> basic scroll (right->left)
      - ls, cs, cst, rs, ss -> scroll modes
      - t / t2 / t4 / t6  -> transfer, default left
      - lt2 / ct4 / rt6 -> transfer с указанием позиции
    delay_spec может быть '5' или '5/4/6'
    Если первая часть до первой '|' не распознана как mode, то считаем всю строку текстом (без mode).
    """
    line = raw_line.rstrip("\n")
    if not line:
        return None
    if line.lstrip().startswith("#"):
        return None

    # Попробуем отделить последний | как разделитель delay (если там числа/слэши)
    delay_list = DEFAULT_DELAYS[:]
    core = line
    last_bar = line.rfind("|")
    if last_bar != -1:
        tail = line[last_bar+1:]
        parsed = parse_delay_spec(tail)
        if parsed != DEFAULT_DELAYS or tail.strip().isdigit():
            delay_list = parsed
            core = line[:last_bar]

    # Теперь определяем mode (если есть) — candidate до первого '|'
    mode_token = ""
    text = core
    first_bar = core.find("|")
    if first_bar != -1:
        candidate = core[:first_bar]
        rest = core[first_bar+1:]
        # распознаём candidate как mode; если не распознано — весь core это text
        if is_mode_token(candidate):
            mode_token = candidate
            text = rest
        else:
            # candidate — часть текста (т.е. строка без mode)
            text = core
            mode_token = ""
    else:
        # нет второго разделителя — возможно весь core это либо mode без текста (invalid) либо plain text
        # считаем plain text
        text = core
        mode_token = ""

    # defaults
    kind = "normal"
    align = "l"
    transfer_n = 8
    scroll_mode = "rs"

    mt = mode_token.strip()

    if mt == "":
        kind = "normal"
        align = "l"
    elif mt in ("l","c","r"):
        kind = "normal"
        align = mt
    elif mt in SCROLL_MODES or mt == "s":
        kind = "scroll"
        scroll_mode = "rs" if mt == "s" else mt
        # special: for cs and cst if text shorter than 8 - auto pad later
    else:
        # check transfer patterns:
        # possibilities: t, t2, t4, t6  OR lt, lt2, ct4, rt6 ...
        if is_transfer_token(mt):
            kind = "transfer"
            # alignment
            if mt[0] in ("l","c","r") and len(mt) > 1 and mt[1] == "t":
                align = mt[0]
                rest = mt[2:]
            elif mt[0] == "t":
                align = "l"
                rest = mt[1:]
            else:
                # fallback
                align = "l"
                rest = mt
            if rest == "":
                transfer_n = 8
            else:
                try:
                    transfer_n = int(rest)
                except Exception:
                    transfer_n = 8
        else:
            # unknown token -> treat whole core as text
            kind = "normal"
            align = "l"
            text = core

    return {
        "kind": kind,
        "align": align,
        "n": transfer_n,
        "mode": scroll_mode,
        "text": text,
        "delays": delay_list
    }

def is_mode_token(tok: str) -> bool:
    if tok in ("l","c","r"):
        return True
    if tok in SCROLL_MODES or tok == "s":
        return True
    if is_transfer_token(tok):
        return True
    return False

def is_transfer_token(tok: str) -> bool:
    # matches t, t2, t4, t6 or lt, lt2, ct4, rt6
    if not tok:
        return False
    if tok[0] == "t":
        # t followed by digits or nothing
        rest = tok[1:]
        if rest == "":
            return True
        return rest.isdigit()
    if tok[0] in ("l","c","r") and len(tok) >= 2 and tok[1] == "t":
        rest = tok[2:]
        if rest == "":
            return True
        return rest.isdigit()
    return False

# ---------- frame generators (PS) ----------

PS_WIDTH = 8

def align_ps(seg: str, align: str) -> str:
    seg = seg[:PS_WIDTH]
    pad = PS_WIDTH - len(seg)
    if align == "r":
        return " " * pad + seg
    if align == "c":
        left = pad // 2
        right = pad - left
        return " " * left + seg + " " * right
    # left
    return seg + " " * pad

def frames_for_entry(entry):
    """
    Возвращает итератор пар (frame_str (len=8), delay_seconds)
    Делает один проход всех кадров, в том порядке, как описано.
    delays (list) применяются циклично по кадрам.
    """
    kind = entry["kind"]
    align = entry["align"]
    n = entry["n"]
    text = entry["text"]
    delays = entry["delays"][:] if entry["delays"] else DEFAULT_DELAYS[:]
    delay_cycle = itertools.cycle(delays)

    if kind == "normal":
        frame = align_ps(text[:PS_WIDTH], align)
        # для нормального режима просто один кадр (delay берём из cycle)
        yield frame, next(delay_cycle)
        return

    if kind == "scroll":
        mode = entry["mode"]
        # cs / cst special: if text shorter than width -> auto pad for appearance modes
        if mode in ("cs", "cst") and len(text) < PS_WIDTH:
            text2 = text.ljust(PS_WIDTH)
        else:
            text2 = text

        if mode in ("rs", "s"):
            # standard right->left (no auto spaces unless text shorter)
            if len(text2) <= PS_WIDTH:
                yield align_ps(text2[:PS_WIDTH], "l"), next(delay_cycle)
            else:
                for i in range(0, len(text2) - PS_WIDTH + 1):
                    yield text2[i:i+PS_WIDTH], next(delay_cycle)
            return

        if mode == "ls":
            # left->right: показываем слева-ориентированные окна, но сдвигаем вправо.
            # Реализация: создаём "padded" копию и пролистываем.
            if len(text2) <= PS_WIDTH:
                yield align_ps(text2[:PS_WIDTH], "l"), next(delay_cycle)
            else:
                # строим кадры, где окно идёт в обратном направлении (имитация левого движения)
                # Простая но рабочая реализация: берем те же фреймы, но инвертируем порядок и левые сдвиги.
                frames = [text2[i:i+PS_WIDTH] for i in range(0, len(text2) - PS_WIDTH + 1)]
                # перевернём порядок, но чтобы движение выглядело с лева направо — выдаём их в обратном порядке
                for fr in reversed(frames):
                    yield fr, next(delay_cycle)
            return

        if mode == "ss":
            # circular scroll: текст+текст и пролистываем len(text) кадров
            if len(text2) <= PS_WIDTH:
                yield align_ps(text2[:PS_WIDTH], "l"), next(delay_cycle)
            else:
                doubled = text2 + text2
                for i in range(0, len(text2)):
                    yield doubled[i:i+PS_WIDTH], next(delay_cycle)
            return

        if mode == "cs":
            # center-appearance: шаги разного размера, центрируем в поле
            center = len(text2) // 2
            # наращивание
            for size in range(1, min(len(text2), PS_WIDTH)+1):
                start = max(0, center - size//2)
                part = text2[start:start+size]
                yield align_ps(part, "c"), next(delay_cycle)
            # убывание
            for size in range(min(len(text2), PS_WIDTH)-1, 0, -1):
                start = max(0, center - size//2)
                part = text2[start:start+size]
                yield align_ps(part, "c"), next(delay_cycle)
            return

        if mode == "cst":
            # cst: сначала cs, затем обычный rs scroll
            # cs:
            yield from (x for x in frames_for_entry({"kind":"scroll","mode":"cs","align":align,"n":n,"text":text,"delays":delays}))
            # затем rs:
            # for rs part reuse logic:
            if len(text2) <= PS_WIDTH:
                yield align_ps(text2[:PS_WIDTH], "l"), next(delay_cycle)
            else:
                for i in range(0, len(text2) - PS_WIDTH + 1):
                    yield text2[i:i+PS_WIDTH], next(delay_cycle)
            return

    if kind == "transfer":
        # transfer: показываем куски длиной n (n = 8,6,4,2...) и каждую часть выравниваем в поле 8 в зависимости от align
        if n <= 0:
            n = 8
        i = 0
        L = len(text)
        if L == 0:
            yield align_ps("", align), next(delay_cycle)
            return
        while i < L:
            seg = text[i:i+n]
            frame = align_ps(seg, align)
            yield frame, next(delay_cycle)
            i += n
        return

# ---------- load files ----------

def load_lines(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.rstrip("\n").strip() and not ln.lstrip().startswith("#")]

def load_rt_list(filename):
    """RT: format 'text|delay' where delay optional. Returns list of (text, delays_list)"""
    items = []
    if not os.path.exists(filename):
        return items
    with open(filename, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            last_bar = line.rfind("|")
            if last_bar != -1:
                tail = line[last_bar+1:]
                delays = parse_delay_spec(tail)
                # if tail not numeric treat whole line as text
                if delays != DEFAULT_DELAYS or tail.strip().isdigit():
                    text = line[:last_bar]
                else:
                    text = line
                    delays = DEFAULT_DELAYS[:]
            else:
                text = line
                delays = DEFAULT_DELAYS[:]
            items.append((text, delays))
    return items

# ---------- main loops ----------

def cycle_ps():
    while True:
        lines = load_lines(ps_file)
        if not lines:
            time.sleep(1)
            continue
        for raw in lines:
            parsed = parse_ps_line(raw)
            if not parsed:
                continue
            # special: if scroll mode cs/cst and text shorter than width -> pad automatically (per spec)
            if parsed["kind"] == "scroll" and parsed["mode"] in ("cs","cst") and len(parsed["text"]) < PS_WIDTH:
                parsed["text"] = parsed["text"].ljust(PS_WIDTH)
            for frame, d in frames_for_entry(parsed):
                send_cmd(f"PS {frame}")
                time.sleep(d)

def cycle_rt():
    # оставляем RT как было — поддерживает выравнивание 'l|text', 'c|text', 'r|text' и scroll modes отдельно
    while True:
        rt_list = load_rt_list(rt_file)
        if not rt_list:
            time.sleep(1)
            continue
        for rt_text, delays in rt_list:
            # по умолчанию просто отправляем RT один раз, заполненный до 64
            txt = (rt_text[:64]).ljust(64)
            # используем первый delay из списка
            delay = delays[0] if delays else DEFAULT_DELAYS[0]
            send_cmd(f"RT {txt}")
            time.sleep(delay)

# ---------- entrypoint ----------

if __name__ == "__main__":
    print("psrt.py стартует. Ждём FIFO rds_ctl...")
    safe_open_fifo()
    threading.Thread(target=cycle_ps, daemon=True).start()
    threading.Thread(target=cycle_rt, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Выход.")
        try:
            if f:
                f.close()
        except Exception:
            pass
