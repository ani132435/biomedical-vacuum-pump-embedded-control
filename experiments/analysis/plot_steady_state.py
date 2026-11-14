import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]

SUMMARY_FILE = (
    ROOT / "experiments" / "results"
    / "final_session_summary.csv"
)

RESULTS_DIR = ROOT / "experiments" / "results"

OUTPUT_FILE = (
    RESULTS_DIR / "final_session_pressure_vs_pwm.png"
)


def load_summary():
    results = []

    with SUMMARY_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            results.append({
                "pwm": int(row["pwm_duty_percent"]),
                "final": float(row["final_pressure_mmhg"]),
                "plateau_detected": (
                    row["plateau_detected"].lower() == "true"
                ),
                "plateau_mean": (
                    float(row["plateau_mean_pressure_mmhg"])
                    if row["plateau_mean_pressure_mmhg"]
                    else None
                ),
                "plateau_start": (
                    float(row["plateau_start_s"])
                    if row["plateau_start_s"]
                    else None
                )
            })

    return results


def main():
    results = load_summary()

    pwm_values = [item["pwm"] for item in results]
    pressures = [
        item["plateau_mean"]
        if item["plateau_detected"]
        else item["final"]
        for item in results
    ]

    labels = [
        (
            f"{item['plateau_mean']:.2f}\n"
            f"Plateau from {item['plateau_start']:.0f} s"
        )
        if item["plateau_detected"]
        else (
            f"{item['final']:.2f}\n"
            "Final reading; no plateau"
        )
        for item in results
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        pwm_values,
        pressures,
        marker="o",
        linewidth=2,
        markersize=8
    )

    for pwm, pressure, label in zip(
        pwm_values, pressures, labels
    ):
        plt.annotate(
            label,
            (pwm, pressure),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=8
        )

    plt.title(
        "Recorded Vacuum Pressure vs PWM Duty Cycle"
    )
    plt.xlabel("PWM Duty Cycle (%)")
    plt.ylabel("Gauge Pressure / Vacuum (mmHg)")

    plt.xticks(pwm_values)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=300)

    print(f"PWM comparison plot saved to:\n{OUTPUT_FILE}")

    plt.show()


if __name__ == "__main__":
    main()
