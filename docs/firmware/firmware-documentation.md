# Firmware Documentation

## 1. Overview

The firmware directory contains MicroPython development code for pressure sensing, motor actuation, PWM characterisation, and preliminary closed-loop control.

The source files represent multiple development iterations. They should **not** be treated as one fully integrated, release-ready firmware application. The sensor-driver interfaces require reconciliation before the complete application can be expected to run unchanged.

## 2. Target Platform and Pin Configuration

The later firmware targets the Raspberry Pi Pico 2W running MicroPython.

| Function | Configuration |
|---|---|
| I2C controller | `I2C(0)` |
| I2C SDA | GP0 |
| I2C SCL | GP1 |
| I2C frequency | 400 kHz |
| Motor PWM | GP2 |
| Motor direction | GP3 and GP4 |
| Motor PWM frequency | 1 kHz |

Pin assignments should be checked against the exact source file and physical hardware revision being used.

## 3. Source-Tree Overview

| File or directory | Purpose |
|---|---|
| `main.py` | Preliminary closed-loop application |
| `controller.py` | PI-controller implementation |
| `motor.py` | Motor PWM and direction control |
| `pressure_sensor.py` | Pressure-sensor abstraction |
| `bmp280.py` | BMP280 driver source |
| `bmp280_sensor.py` | Alternative BMP280 implementation |
| `config.py` | Control and hardware configuration |
| `modes.py` | Preliminary operating-mode definitions |
| `state_machine.py` | Basic state representation |
| `control/pump.py` | Modular pump PWM abstraction |
| `control/valve.py` | Preliminary valve-control module |
| `tests/` | Sensor, I2C, PWM, and pump experiments |

The repository may contain experimental scripts and alternate implementations alongside these modules. Inspect the relevant source before selecting an entry point.

## 4. Motor Control

The inspected `Motor` implementation provides:

- PWM initialisation.
- Forward and reverse direction selection.
- Motor stop operation.
- Speed control through a percentage duty-cycle command.

The inspected implementation configures PWM at 1 kHz and uses MicroPython's `duty_u16()` interface to apply the requested duty cycle.

The separate `control/pump.py` module provides another PWM-based pump abstraction.

Confirm the driver wiring, supply voltage, current capability, and safe operating conditions before running motor commands on hardware.

## 5. Pressure Measurement

The BMP280 measures absolute pressure. The intended measurement sequence is:

1. Read absolute pressure from the sensor.
2. Establish an atmospheric-pressure reference.
3. Calculate gauge pressure by subtracting the atmospheric reference.
4. Use the resulting measurement for monitoring or feedback.

Multiple BMP280 driver implementations are present in the repository. Their APIs are not identical, so the selected driver and calling code must be made consistent.

## 6. PWM Characterisation

The experimental firmware includes a PWM characterisation routine.

Documented test settings include:

- PWM duty-cycle levels from 40% to 100%.
- A nominal 30-second test period at each PWM level.
- A final 10-second analysis window.
- A nominal sampling interval of 0.1 seconds.
- Atmospheric-reference reset checks.
- A software vacuum cut-off condition.

The routine calculates pressure statistics such as average pressure, final-window average pressure, and the most negative observed gauge pressure.

Refer to the experimental methodology and raw datasets for the specific test procedure and results.

## 7. Preliminary PI Controller

The `PIController` class implements proportional-integral control:

`u(t) = Kp * e(t) + Ki * integral(e(t) dt)`

The implementation includes integral accumulation and clamping. The inspected `main.py` contains a preliminary feedback loop with a target pressure, baseline PWM command, and PWM limits.

The presence of a PI algorithm in the source code does not establish that it has been tuned or validated on the physical prototype. No validated closed-loop performance is claimed.

## 8. Operating Modes and State Machine

The `modes.py` file defines stimulation, expression, and custom mode identifiers.

The `state_machine.py` file defines OFF, STIMULATION, EXPRESSION, and ERROR states.

These are preliminary software structures, not evidence of fully implemented or validated operating modes.

## 9. Known Source-Integration Limitations

The repository contains several sensor-driver implementations with different interfaces.

In the inspected source snapshot:

- `main.py` and experimental test code call `PressureSensor(i2c, alpha=0.85)` and expect a `calibrate_atmosphere()` method.
- The inspected `pressure_sensor.py` implementation accepts `i2c` and does not expose that same constructor argument or calibration method.
- The root `bmp280.py` uses a configuration-based driver structure, while `bmp280_sensor.py` exposes a different interface.

These differences indicate that the source tree contains development snapshots requiring interface reconciliation. Do not assume that every module can be imported and run together without modification.

## 10. Firmware Status

| Function | Status |
|---|---|
| I2C sensor interface | Developed in source |
| BMP280 drivers | Multiple implementations; interfaces need consolidation |
| Motor PWM control | Implemented in source |
| Experimental PWM characterisation | Performed |
| PI-control algorithm | Implemented in source; physical tuning incomplete |
| Operating-mode definitions | Preliminary |
| State-machine structure | Preliminary |
| Valve integration | Incomplete |
| Unified firmware integration | Requires further work |

## 11. Safe Reproduction Notes

- Inspect the selected driver and its calling code before combining modules.
- Confirm the board pinout and physical wiring before connecting the pump or valve.
- Use a correctly rated supply and appropriate protection for inductive loads.
- Test sensor communication and motor-control signals independently before attempting closed-loop operation.
- Do not operate the prototype on a person. This is an engineering development platform, not a validated medical device.

## 12. Related Documentation

- [Hardware Design](../hardware/hardware-design.md)
- [System Architecture](../architecture/system-architecture.md)
- [Project Status and Future Work](../project-status.md)
- [Reproduction and Simulation Guide](../reproduction/simulation-and-reproduction-guide.md)
