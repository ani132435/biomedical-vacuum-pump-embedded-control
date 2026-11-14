import csv
import re
import statistics
from pathlib import Path
from collections import defaultdict


ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT / "experiments" / "raw_data"
RESULTS_DIR = ROOT / "experiments" / "results"

FILES = {
    "Experiment 01": RAW_DIR / "EXPERIMENT 01.txt",
    "Experiment 02": RAW_DIR / "EXPERIMENT-02.txt",
    "Experiment 03": RAW_DIR / "EXPERIMENT-03.txt",
}

MEASUREMENT_PATTERN = re.compile(
    r"^\s*PWM:\s*(\d+)\s*%\s*\|\s*"
    r"ABS:\s*(-?[\d.]+)\s*mmHg\s*\|\s*"
    r"VAC:\s*(-?[\d.]+)\s*mmHg",
    re.IGNORECASE
)

AVERAGE_PATTERN = re.compile(
    r"Average vacuum:\s*(-?[\d.]+)\s*mmHg",
    re.IGNORECASE
)

MAXIMUM_PATTERN = re.compile(
    r"Maximum measured vacuum:\s*(-?[\d.]+)\s*mmHg",
    re.IGNORECASE
)


def parse_experiment(name, path):

    if not path.exists():
        raise FileNotFoundError(path)

    segments = []
    current_segment = None
    reported_averages = []
    reported_maxima = []

    with path.open("r", encoding="utf-8-sig") as file:

        for line_number, line in enumerate(file, start=1):

            match = MEASUREMENT_PATTERN.search(line)

            if match:
                pwm = int(match.group(1))
                absolute = float(match.group(2))
                vacuum = float(match.group(3))

                if (
                    current_segment is None
                    or current_segment["pwm"] != pwm
                ):
                    current_segment = {
                        "experiment": name,
                        "segment": len(segments) + 1,
                        "pwm": pwm,
                        "measurements": []
                    }
                    segments.append(current_segment)

                current_segment["measurements"].append({
                    "experiment": name,
                    "segment": current_segment["segment"],
                    "pwm_duty_percent": pwm,
                    "sample_index": len(
                        current_segment["measurements"]
                    ) + 1,
                    "source_line": line_number,
                    "absolute_pressure_mmhg": absolute,
                    "vacuum_mmhg": vacuum
                })

            average = AVERAGE_PATTERN.search(line)
            if average:
                reported_averages.append(float(average.group(1)))

            maximum = MAXIMUM_PATTERN.search(line)
            if maximum:
                reported_maxima.append(float(maximum.group(1)))

    return segments, reported_averages, reported_maxima


def calculate_summary(segment, reported_average, reported_maximum):

    readings = segment["measurements"]
    pressures = [item["vacuum_mmhg"] for item in readings]

    calculated_mean = statistics.mean(pressures)
    calculated_minimum = min(pressures)
    calculated_maximum = max(pressures)

    return {
        "experiment": segment["experiment"],
        "segment": segment["segment"],
        "pwm_duty_percent": segment["pwm"],
        "sample_count": len(pressures),
        "first_vacuum_mmhg": pressures[0],
        "last_vacuum_mmhg": pressures[-1],
        "mean_vacuum_mmhg": calculated_mean,
        "std_dev_mmhg": (
            statistics.stdev(pressures)
            if len(pressures) > 1 else 0.0
        ),
        "most_negative_vacuum_mmhg": calculated_minimum,
        "least_negative_vacuum_mmhg": calculated_maximum,
        "reported_average_mmhg": (
            reported_average if reported_average is not None else ""
        ),
        "average_difference_mmhg": (
            calculated_mean - reported_average
            if reported_average is not None else ""
        ),
        "reported_maximum_vacuum_mmhg": (
            reported_maximum if reported_maximum is not None else ""
        ),
        "maximum_difference_mmhg": (
            calculated_minimum - reported_maximum
            if reported_maximum is not None else ""
        )
    }


def main():

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    all_measurements = []
    all_summaries = []

    print("\n========================================")
    print(" ARCHIVED EXPERIMENT ANALYSIS")
    print("========================================")

    for name, path in FILES.items():

        segments, averages, maxima = parse_experiment(name, path)

        print(f"\n{name}")
        print(f"Measurement segments: {len(segments)}")
        print(f"Total readings: {sum(len(s['measurements']) for s in segments)}")

        if len(averages) != len(segments):
            print(
                "NOTE: Reported averages do not map one-to-one "
                "to measurement segments."
            )

        if len(maxima) != len(segments):
            print(
                "NOTE: Reported maximum values do not map one-to-one "
                "to measurement segments."
            )

        for index, segment in enumerate(segments):

            all_measurements.extend(segment["measurements"])

            reported_average = (
                averages[index] if index < len(averages) else None
            )
            reported_maximum = (
                maxima[index] if index < len(maxima) else None
            )

            summary = calculate_summary(
                segment,
                reported_average,
                reported_maximum
            )

            all_summaries.append(summary)

            print(
                f"  Segment {segment['segment']}: "
                f"{segment['pwm']}% PWM, "
                f"{summary['sample_count']} samples"
            )
            print(
                f"    Recalculated mean: "
                f"{summary['mean_vacuum_mmhg']:.3f} mmHg"
            )
            print(
                f"    Most negative: "
                f"{summary['most_negative_vacuum_mmhg']:.2f} mmHg"
            )
            print(
                f"    Final reading: "
                f"{summary['last_vacuum_mmhg']:.2f} mmHg"
            )

            if reported_average is not None:
                print(
                    f"    Reported mean: {reported_average:.3f} mmHg"
                )
                print(
                    f"    Mean difference: "
                    f"{summary['average_difference_mmhg']:.3f} mmHg"
                )

            if reported_maximum is not None:
                print(
                    f"    Reported maximum vacuum: "
                    f"{reported_maximum:.2f} mmHg"
                )
                print(
                    f"    Difference from most negative reading: "
                    f"{summary['maximum_difference_mmhg']:.3f} mmHg"
                )

    measurement_file = RESULTS_DIR / "archived_measurements.csv"
    summary_file = RESULTS_DIR / "archived_experiment_summary.csv"

    if all_measurements:
        with measurement_file.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=list(all_measurements[0].keys())
            )
            writer.writeheader()
            writer.writerows(all_measurements)

    if all_summaries:
        with summary_file.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=list(all_summaries[0].keys())
            )
            writer.writeheader()
            writer.writerows(all_summaries)

    print("\n========== EXPORTED FILES ==========")
    print(measurement_file)
    print(summary_file)
    print("\nArchived analysis completed.")


if __name__ == "__main__":
    main()
