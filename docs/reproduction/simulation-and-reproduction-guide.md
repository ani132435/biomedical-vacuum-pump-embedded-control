# Reproduction and Simulation Guide

## 1. Purpose

This guide explains how another student or engineer can obtain the repository, inspect the development files, and reproduce the documented experimental-data analysis.

It distinguishes three different activities:

- **Reproducing analysis:** Processing measurements already recorded during experiments and regenerating plots or summary statistics.
- **Hardware reproduction:** Rebuilding the physical prototype from verified component and wiring information.
- **Simulation:** Running a mathematical or software model to predict system behaviour.

These activities are related, but they are not interchangeable. The current repository documents experimental analysis and preliminary design work. It does not claim to provide a validated end-to-end simulation of the physical pump.

## 2. Repository

Source repository:

[Biomedical Vacuum Pump - Embedded Control System](https://github.com/ani132435/biomedical-vacuum-pump-embedded-control)

Clone the repository using Git:

```bash
git clone https://github.com/ani132435/biomedical-vacuum-pump-embedded-control.git
cd biomedical-vacuum-pump-embedded-control
```

Inspect the repository:

```bash
git status
git log --oneline -5
```

## 3. Software Prerequisites

The repository includes MicroPython firmware source and Python-based experimental analysis material.

Recommended tools:

- Git, for cloning and version control.
- Python 3, for data inspection and analysis.
- A code editor such as Visual Studio Code.
- MicroPython-compatible tooling and a supported USB connection, if working with the Pico 2W firmware.
- FreeCAD, if inspecting the mechanical CAD files.
- KiCad, if inspecting the historical schematic project.

The exact Python packages required depend on the analysis script being used. Inspect the imports at the top of each script before installing dependencies.

Common scientific Python packages include NumPy, pandas, and Matplotlib.

Create an isolated Python environment from the repository root:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

If the selected analysis script imports NumPy, pandas, and Matplotlib, install them using:

```bash
python -m pip install numpy pandas matplotlib
```

Install any additional dependencies required by the specific script. No single dependency list should be assumed to cover every experimental script in this development repository.

## 4. Understanding the Repository Data

| Location | Contents and use |
|---|---|
| `experiments/raw_data/` | Archived experimental logs and source measurements |
| `experiments/analysis/` | Python analysis and plotting scripts |
| `experiments/results/` | Generated plots and result files |
| `docs/experiments/` | Experimental procedure, methodology, and interpretation |
| `firmware/` | MicroPython development source and hardware tests |
| `docs/hardware/` | Component information and hardware-development notes |
| `mechanical/` | Preliminary CAD files and measurement references |
| `electronics/kicad/` | Earlier ESP32-based schematic reference |

Some raw files are archived text logs rather than clean, uniform CSV files. Inspect each file's header, delimiter, units, and measurement format before importing it into a data-analysis script.

## 5. Reproducing the Experimental Analysis

A practical workflow is:

1. Read [Experimental Methodology](../experiments/experimental-methodology.md) to understand the test sequence and measurement conditions.
2. Inspect `experiments/raw_data/` and identify the dataset corresponding to the result you want to reproduce.
3. Inspect the relevant script in `experiments/analysis/` and note its expected input filename, column names, units, and output location.
4. Install the dependencies imported by that script.
5. Run the script from the repository root unless its comments or path handling specify a different working directory.
6. Compare the generated output with the committed files in `experiments/results/`.
7. Record differences caused by data cleaning, filtering, rounding, or script-version changes.

A supplementary dataset used during development has a structure similar to this:

| Column | Meaning |
|---|---|
| `elapsed_s` | Elapsed time in seconds |
| `pwm_duty_percent` | Motor PWM duty cycle in percent |
| `vacuum_mmhg` | Recorded gauge pressure in mmHg |

This is an example of a documented dataset format, not a guarantee that every archived raw-data file uses the same schema. Check each actual file before applying a script.

## 6. Interpreting the Results

The intended pressure range was approximately **-50 to -200 mmHg gauge pressure**.

The documented prototype experiments recorded approximately **-3 to -11 mmHg gauge pressure** under the tested conditions.

The committed plots and analysis therefore describe preliminary prototype behaviour. They do not demonstrate that the intended pressure range was achieved.

When reproducing results, preserve the distinction between:

- Component specifications supplied by manufacturers.
- Measurements recorded during prototype experiments.
- Targets defined for the intended application.
- Values generated by a later mathematical or simulation model.

Do not combine these categories as if they were interchangeable measurements.

## 7. Simulation: Current Scope and Limitations

The current repository should be treated as an experimental-data and embedded-development archive, not as a completed simulation package.

The presence of control code, experimental plots, or a system architecture diagram does not by itself provide a mathematical plant model.

A credible pump simulation would require, at minimum:

- A defined plant model relating motor command to pressure response.
- Identified parameters derived from suitable measurements.
- Explicit assumptions about pump behaviour, pneumatic volume, leakage, tubing, and load conditions.
- A documented numerical implementation and reproducible simulation settings.
- Comparison between model output and independent experimental measurements.

A future simulation could begin with a simple empirical model fitted to measured PWM-versus-pressure response, then be refined using time-series data.

Such a model must be labelled as an approximation and validated against separate measurements before it is used to make performance claims.

No ready-to-run, validated Simulink or equivalent end-to-end pump model is claimed by this guide.

If a simulator or model is added later, document its software version, model files, parameter sources, solver settings, initial conditions, and validation procedure here.

## 8. Hardware Reproduction Warning

The hardware documentation records components and selected firmware pin assignments, but it is not a complete verified build manual.

In particular:

- The KiCad schematic is an earlier ESP32-based design reference, not the final Pico 2W as-built wiring.
- The complete power-distribution and wiring arrangement must be independently verified.
- Solenoid-valve integration is incomplete.
- The firmware source contains multiple BMP280 driver interfaces that require reconciliation.
- The PI controller has not been physically tuned and validated.

Do not connect or operate hardware solely by copying a pin list from the documentation. Verify the circuit, ratings, polarity, grounding, current limits, and protection requirements before applying power.

## 9. Suggested Contribution Workflow

If you extend the project:

1. Create a separate Git branch for your changes.
2. Preserve original raw datasets; write processed data to a separate output location.
3. Record the experiment date, hardware configuration, firmware revision, sampling interval, and units.
4. Keep scripts reproducible by documenting dependencies and input paths.
5. Label simulated, calculated, and experimentally measured results separately.
6. Update documentation when a hardware interface or firmware API changes.
7. Submit changes with a concise commit message describing what changed.

## 10. Related Documentation

- [System Architecture](../architecture/system-architecture.md)
- [Hardware Design](../hardware/hardware-design.md)
- [Firmware Documentation](../firmware/firmware-documentation.md)
- [Experimental Methodology](../experiments/experimental-methodology.md)
- [Results and Analysis](../experiments/results-and-analysis.md)
- [Project Status and Future Work](../project-status.md)

## 11. Disclaimer

This repository documents an academic engineering prototype. It is not a certified or clinically validated medical device and must not be used for medical applications.
