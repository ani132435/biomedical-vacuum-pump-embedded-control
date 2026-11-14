# Project Status and Future Work

## 1. Project Stage

The project is an engineering prototype and experimental development effort focused on pressure-monitored vacuum generation, embedded motor control, and preliminary pressure regulation.

The repository preserves hardware notes, MicroPython development code, experimental datasets, analysis, and preliminary mechanical/electrical design work. The system is not a validated medical device.

## 2. Completed and Documented Work

### 2.1 Hardware and Prototyping

- Developed a vacuum-pump prototype around a KMDP-U1-24V pump.
- Interfaced a BMP280 pressure sensor during development.
- Used a Raspberry Pi Pico 2W as the later embedded controller.
- Developed DC motor actuation using an L298N module.
- Identified and measured the CKS5001/04 solenoid valve.
- Performed physical measurements to support preliminary CAD modelling.

### 2.2 Embedded Development

- Developed MicroPython sensor- and motor-control code.
- Implemented PWM-based motor speed-control functions.
- Developed pressure-acquisition and monitoring routines.
- Created a preliminary PI-controller implementation.
- Developed preliminary operating-mode and state-machine structures.

### 2.3 Experimental Analysis

- Conducted PWM-based vacuum characterisation.
- Preserved archived experimental measurements.
- Transcribed a supplementary final-session dataset from original plotting scripts.
- Developed Python scripts for processing and plotting experimental data.
- Documented the experimental methodology and observed results.

### 2.4 Mechanical and Electrical Design

- Developed preliminary FreeCAD models for the pump motor sleeve and valve.
- Created an earlier ESP32-based KiCad schematic reference.

## 3. Experimental Performance

The intended application pressure range was approximately **-50 to -200 mmHg gauge pressure**.

The documented prototype measurements were approximately **-3 to -11 mmHg gauge pressure** under the recorded test conditions. The prototype therefore did not achieve its intended pressure range during those experiments.

The experiments provide preliminary information about pressure response as PWM duty cycle changes. They do not establish clinical performance, medical suitability, or validated closed-loop regulation.

See [Experimental Methodology](experiments/experimental-methodology.md) and [Results and Analysis](experiments/results-and-analysis.md).

## 4. Work Incomplete or Requiring Validation

- Complete electrical and pneumatic integration of the solenoid valve.
- Reconcile and consolidate the BMP280 driver interfaces.
- Integrate the firmware into one consistent application.
- Tune the PI controller and validate physical closed-loop operation.
- Complete and test stimulation and expression operating modes.
- Verify the complete electrical wiring and power-distribution arrangement.
- Investigate the gap between intended and measured vacuum.
- Fabricate and fit-test the preliminary mechanical CAD components.
- Establish repeatability and reliability through controlled testing.

## 5. Recommended Future Work

### 5.1 Hardware Verification

1. Produce and verify a complete as-built wiring diagram for the Pico 2W, sensor, motor driver, pump, and power supplies.
2. Verify supply ratings, current capability, grounding, switching devices, and protection.
3. Complete the valve driver and pneumatic integration.
4. Fabricate and fit-test the mechanical components.

### 5.2 Sensor and Firmware Integration

1. Select one BMP280 driver implementation.
2. Define one consistent pressure-sensor API, including atmospheric-reference handling.
3. Test sensor readings and calibration independently.
4. Consolidate the motor, sensor, controller, and state-management modules.
5. Add fault handling and hardware safety interlocks before integrated operation.

### 5.3 Characterisation and Control

1. Repeat pump characterisation under documented, controlled conditions.
2. Investigate leakage, tubing, pneumatic restrictions, pump loading, and sensor-reference effects that may explain the measured pressure range.
3. Use measured system response to select and tune PI-controller parameters.
4. Validate closed-loop behaviour using independent pressure monitoring and suitable hardware safeguards.
5. Evaluate repeatability, transient response, stability, and achievable vacuum range.

## 6. Simulation and Reproduction Status

The repository contains experimental datasets, analysis material, and plots that can be inspected and used to reproduce the documented data-processing work.

The repository should not currently be described as containing a validated end-to-end plant simulation or a verified digital model of the physical pump.

Reproducing recorded plots is different from simulating the physical system or validating a controller against a plant model.

See the [Reproduction and Simulation Guide](reproduction/simulation-and-reproduction-guide.md).

## 7. Scope and Disclaimer

This repository documents an academic engineering prototype and its development process. It is not a certified or validated medical device, has not undergone clinical validation, and must not be used for medical applications or to make clinical claims.
