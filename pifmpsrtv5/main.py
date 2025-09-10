from parser import parse_line
from ps_modes import generate_ps_frames
from transfers import generate_transfer_frames
from rt_modes import generate_rt_frames

def main():
    print("=== PS ===")
    with open("ps.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            mode, text, times = parse_line(line)

            if mode.startswith("t"):  # переносы
                frames = generate_transfer_frames(mode, text)
            else:  # обычные PS режимы
                frames = generate_ps_frames(mode, text, times)

            print(f"\nMode={mode} Text='{text}' Times={times}")
            for idx, fr in enumerate(frames):
                print(f" {idx+1:02d}: {fr}")

    print("\n=== RT ===")
    with open("rt.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            mode, text, times = parse_line(line)
            frames = generate_rt_frames(mode, text, times)

            print(f"\nMode={mode} Text='{text}' Times={times}")
            for idx, fr in enumerate(frames):
                print(f" {idx+1:02d}: {fr}")

if __name__ == "__main__":
    main()
