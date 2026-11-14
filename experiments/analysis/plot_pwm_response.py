import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT / "experiments" / "raw_data"
    / "supplementary" / "final_lab_session_pwm.csv"
)

RESULTS_DIR = ROOT / "experiments" / "results"
OUTPUT_FILE = RESULTS_DIR / "final_session_pwm_response.png"


def load_data():
    grouped = defaultdict(list)

    with DATA_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            pwm = int(row["pwm_duty_percent"])
            time = float(row["elapsed_s"])
            vacuum = float(row["vacuum_mmhg"])

            grouped[pwm].append((time, vacuum))

    for pwm in grouped:
        grouped[pwm].sort(key=lambda point: point[0])

    return grouped


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_data()

    plt.figure(figsize=(9, 5.5))

    markers = {
        80: "o",
        90: "s",
        100: "^"
    }

    for pwm, measurements in sorted(data.items()):
        times = [point[0] for point in measurements]
        vacuum = [point[1] for point in measurements]

        plt.plot(
            times,
            vacuum,
            marker=markers.get(pwm, "o"),
            linewidth=2,
            markersize=5,
            label=f"{pwm}% PWM"
        )

    plt.title(
        "Vacuum Pressure Response at Different PWM Duty Cycles"
    )
    plt.xlabel("Elapsed Time (s)")
    plt.ylabel("Gauge Pressure / Vacuum (mmHg)")

    plt.xlim(left=0)
    plt.ylim(bottom=-12, top=0.5)

    plt.xticks(range(0, 16, 1))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Response plot saved to:\n{OUTPUT_FILE}")

    plt.show()


if __name__ == "__main__":
    main()
