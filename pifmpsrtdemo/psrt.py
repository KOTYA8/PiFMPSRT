import threading
import time
from pifmpsrt.ps_cycle import cycle_ps
from pifmpsrt.rt_cycle import cycle_rt

PS_FILE = "pifmpsrt/ps.txt"
RT_FILE = "pifmpsrt/rt.txt"
FIFO = "/tmp/rds_ctl"   # путь к FIFO PiFmRds

def main():
    t1 = threading.Thread(target=cycle_ps, args=(PS_FILE, FIFO), daemon=True)
    t2 = threading.Thread(target=cycle_rt, args=(RT_FILE, FIFO), daemon=True)
    t1.start()
    t2.start()

    print("✅ PS/RT циклы запущены. Нажмите Ctrl+C для выхода.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Остановлено пользователем")

if __name__ == "__main__":
    main()
