import time
import threading
import subprocess

# Пути к rds_ctl (проверьте путь!)
RDS_CTL = "./rds_ctl"

# Списки PS и RT
ps_list = ["RADIOPI", "STATION", "HELLO", "TEST123", "MUSIC"]
rt_list = [
    "Добро пожаловать на FM через Raspberry Pi!",
    "Сейчас играет тестовый трек.",
    "RDS работает в реальном времени.",
    "Переключение текста каждые 7 секунд.",
    "Привет из Python!"
]

# Интервалы в секундах
ps_delay = 5
rt_delay = 7

def cycle_ps():
    """Цикл смены PS"""
    while True:
        for ps in ps_list:
            subprocess.run([RDS_CTL, "PS", ps])
            print(f"[PS] -> {ps}")
            time.sleep(ps_delay)

def cycle_rt():
    """Цикл смены RT"""
    while True:
        for rt in rt_list:
            subprocess.run([RDS_CTL, "RT", rt])
            print(f"[RT] -> {rt}")
            time.sleep(rt_delay)

def cycle_ta():
    """Пример работы с TA"""
    while True:
        subprocess.run([RDS_CTL, "TA", "ON"])
        print("[TA] -> ON")
        time.sleep(10)
        subprocess.run([RDS_CTL, "TA", "OFF"])
        print("[TA] -> OFF")
        time.sleep(20)

if __name__ == "__main__":
    # Запускаем потоки
    threading.Thread(target=cycle_ps, daemon=True).start()
    threading.Thread(target=cycle_rt, daemon=True).start()
    threading.Thread(target=cycle_ta, daemon=True).start()

    # Чтобы программа не завершалась
    while True:
        time.sleep(1)
