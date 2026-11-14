import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "experiments" / "results" / "archived_measurements.csv"
OUTPUT_DIR = ROOT / "experiments" / "results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


with DATA_FILE.open("r", encoding="utf-8-sig") as file:
    measurements = list(csv.DictReader(file))


experiments = ["Experiment 01", "Experiment 02", "Experiment 03"]

for experiment in experiments:

    experiment_data = [
        row for row in measurements
        if row["experiment"] == experiment
    ]

    if not experiment_data:
        continue

    plt.figure(figsize=(10, 5))

    for segment in sorted(
        {row["segment"] for row in experiment_data},
        key=int
    ):

        segment_data = [
            row for row in experiment_data
            if row["segment"] == segment
        ]

        sample_indices = [
            int(row["sample_index"])
            for row in segment_data
        ]

        pressures = [
            float(row["vacuum_mmhg"])
            for row in segment_data
        ]

        pwm = segment_data[0]["pwm_duty_percent"]

        plt.plot(
            sample_indices,
            pressures,
            linewidth=1.5,
            label=f"{pwm}% PWM"
        )

    plt.title(f"{experiment} - Vacuum Pressure Response")
    plt.xlabel("Sample Index")
    plt.ylabel("Gauge Pressure (mmHg)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_file = OUTPUT_DIR / (
        experiment.lower().replace(" ", "_") + "_response.png"
    )

    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Saved: {output_file}")

print("\nArchived response plots generated.")
