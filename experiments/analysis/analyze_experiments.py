import csv
import statistics
from pathlib import Path


# ============================================================
# PATHS AND ANALYSIS SETTINGS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    ROOT
    / "experiments"
    / "raw_data"
    / "supplementary"
    / "final_lab_session_pwm.csv"
)

RESULTS_DIR = ROOT / "experiments" / "results"

OUTPUT_FILE = RESULTS_DIR / "final_session_summary.csv"

# Operational plateau-detection threshold.
# This is an analysis heuristic, not a sensor accuracy specification.
PLATEAU_TOLERANCE = 0.02  # mmHg
MIN_PLATEAU_SAMPLES = 3


# ============================================================
# LOAD EXPERIMENTAL DATA
# ============================================================

def load_data(file_path):

    if not file_path.exists():
        raise FileNotFoundError(
            f"Experimental data not found: {file_path}"
        )

    records = []

    with file_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "elapsed_s",
            "pwm_duty_percent",
            "vacuum_mmhg"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV is missing one or more required columns."
            )

        for row in reader:
            records.append({
                "time": float(row["elapsed_s"]),
                "pwm": int(row["pwm_duty_percent"]),
                "pressure": float(row["vacuum_mmhg"])
            })

    if not records:
        raise ValueError("No experimental measurements found.")

    return records


# ============================================================
# DATA VALIDATION
# ============================================================

def validate_data(records):

    grouped = {}

    for record in records:
        grouped.setdefault(record["pwm"], []).append(record)

    print("\n========== DATA VALIDATION ==========")

    for pwm, samples in sorted(grouped.items()):

        samples.sort(key=lambda item: item["time"])

        times = [sample["time"] for sample in samples]

        duplicates = len(times) != len(set(times))

        intervals = [
            times[i + 1] - times[i]
            for i in range(len(times) - 1)
        ]

        incorrect_intervals = [
            interval for interval in intervals
            if interval != 1.0
        ]

        print(f"\nPWM: {pwm}%")
        print(f"Number of samples: {len(samples)}")
        print(f"Duplicate timestamps: {duplicates}")
        print(f"One-second intervals verified: {not incorrect_intervals}")

        if duplicates or incorrect_intervals:
            print("WARNING: Check the sampling sequence.")

    return grouped


# ============================================================
# STEADY-STATE / PLATEAU DETECTION
# ============================================================

def detect_plateau(samples):

    final_pressure = samples[-1]["pressure"]

    for index in range(len(samples)):

        remaining = samples[index:]

        if len(remaining) < MIN_PLATEAU_SAMPLES:
            continue

        within_tolerance = all(
            abs(sample["pressure"] - final_pressure)
            <= PLATEAU_TOLERANCE
            for sample in remaining
        )

        if within_tolerance:
            return {
                "start_time": samples[index]["time"],
                "sample_count": len(remaining),
                "mean_pressure": statistics.mean(
                    sample["pressure"] for sample in remaining
                )
            }

    return None


# ============================================================
# CALCULATE EXPERIMENTAL STATISTICS
# ============================================================

def analyze_group(pwm, samples):

    samples.sort(key=lambda item: item["time"])

    pressures = [
        sample["pressure"] for sample in samples
    ]

    initial_pressure = pressures[0]
    final_pressure = pressures[-1]

    plateau = detect_plateau(samples)

    return {
        "pwm_duty_percent": pwm,
        "sample_count": len(samples),
        "initial_pressure_mmhg": initial_pressure,
        "final_pressure_mmhg": final_pressure,
        "mean_pressure_mmhg": statistics.mean(pressures),
        "std_dev_mmhg": statistics.stdev(pressures),
        "most_negative_pressure_mmhg": min(pressures),
        "least_negative_pressure_mmhg": max(pressures),
        "vacuum_magnitude_increase_mmhg": (
            initial_pressure - final_pressure
        ),
        "plateau_detected": plateau is not None,
        "plateau_start_s": (
            plateau["start_time"] if plateau else ""
        ),
        "plateau_mean_pressure_mmhg": (
            plateau["mean_pressure"] if plateau else ""
        )
    }


# ============================================================
# EXPORT RESULTS
# ============================================================

def export_results(results):

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = list(results[0].keys())

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nSummary exported to:\n{OUTPUT_FILE}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n========================================")
    print(" FINAL LAB SESSION - EXPERIMENT ANALYSIS")
    print("========================================")

    records = load_data(DATA_FILE)

    grouped = validate_data(records)

    results = []

    for pwm, samples in sorted(grouped.items()):

        result = analyze_group(pwm, samples)
        results.append(result)

    print("\n========== EXPERIMENTAL RESULTS ==========")

    for result in results:

        print(f"\nPWM DUTY: {result['pwm_duty_percent']}%")
        print(f"Samples: {result['sample_count']}")
        print(
            f"Mean pressure: "
            f"{result['mean_pressure_mmhg']:.3f} mmHg"
        )
        print(
            f"Standard deviation: "
            f"{result['std_dev_mmhg']:.3f} mmHg"
        )
        print(
            f"Final pressure: "
            f"{result['final_pressure_mmhg']:.2f} mmHg"
        )
        print(
            f"Most negative pressure: "
            f"{result['most_negative_pressure_mmhg']:.2f} mmHg"
        )

        if result["plateau_detected"]:
            print(
                f"Possible plateau begins at: "
                f"{result['plateau_start_s']} s"
            )
            print(
                f"Plateau mean: "
                f"{result['plateau_mean_pressure_mmhg']:.3f} mmHg"
            )
        else:
            print("Possible plateau: Not detected")

    export_results(results)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
