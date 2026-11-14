Firmware Documentation
1. Overview
The firmware repository contains MicroPython development code
for pressure sensing, motor actuation, PWM characterisation
and preliminary closed-loop control.
The source files represent multiple development iterations.
They should not be treated as one fully integrated firmware
release.
2. Platform
The later firmware targets the Raspberry Pi Pico 2W.
Function
Configuration
I2C controller
I2C(0)
SDA
GP0
SCL
GP1
I2C frequency
400 kHz
Motor PWM
GP2
Motor direction
GP3 and GP4
Motor PWM frequency
1 kHz
3. Source Structure
File
Purpose
main.py
Preliminary closed-loop application
controller.py
PI controller
motor.py
Motor PWM and direction control
pressure_sensor.py
Pressure sensor abstraction
bmp280.py
BMP280 driver source
bmp280_sensor.py
Alternative BMP280 implementation
config.py
Control configuration
modes.py
Operating-mode definitions
state_machine.py
Basic state representation
control/pump.py
Modular pump PWM abstraction
control/valve.py
Preliminary valve-control module
tests/
Sensor, I2C, PWM and pump experiments
4. Motor Control
The Motor class provides:
- PWM initialisation.
- Forward and reverse direction selection.
- Motor stop operation.
- Speed control through a percentage duty-cycle command.
The inspected implementation configures PWM at 1 kHz and
uses duty_u16() to apply the requested duty cycle.
The separate control/pump.py module provides a modular
PWM-based pump abstraction.
5. Pressure Measurement
The BMP280 measures absolute pressure.
The intended processing sequence is:
1. Acquire an absolute pressure reading.
2. Establish an atmospheric reference.
3. Calculate gauge pressure.
4. Use the pressure measurement for monitoring or feedback.
Multiple BMP280 driver implementations are present in the
repository, reflecting different development iterations.
6. PWM Characterisation
The experimental firmware includes a PWM characterisation routine.
Its documented settings include:
- PWM levels from 40% to 100%.
- A nominal 30-second test period per PWM level.
- A final 10-second analysis window.
- A nominal 0.1-second sampling interval.
- Atmospheric reset verification.
- A software vacuum cutoff condition.
The routine calculates average pressure, final-window average
pressure and the most negative observed gauge pressure.
Experimental datasets and analysis are documented separately
under docs/experiments/.
7. PI Controller
The PIController class implements proportional-integral control:
\[u(t)=K_p e(t)+K_i\int e(t)\,dt\]
The implementation includes integral accumulation and clamping.
The inspected main.py contains a preliminary feedback loop
with target pressure, baseline PWM and PWM limits.
The presence of this algorithm in source code does not establish
that it was successfully tuned or validated on the physical
prototype. No validated PI performance is claimed.
8. Operating Modes and State Machine
The modes.py file defines stimulation, expression and custom
mode identifiers.
The state_machine.py file defines OFF, STIMULATION,
EXPRESSION and ERROR states.
These are preliminary software structures, not evidence of
fully implemented or validated operating modes.
9. Source Integration Limitations
The repository contains several sensor-driver implementations.
The inspected main.py and experimental test code call
PressureSensor(i2c, alpha=0.85) and expect a
calibrate_atmosphere() method.
However, the inspected pressure_sensor.py implementation
does not expose that interface.
The root bmp280.py also uses a configuration-based driver
structure, while bmp280_sensor.py exposes a different
interface.
These differences indicate that the source tree contains
development snapshots requiring interface reconciliation
before being treated as one executable firmware application.
10. Firmware Status
Function
Status
I2C sensor interface
Developed
BMP280 drivers
Multiple implementations present
Motor PWM control
Implemented in source
Experimental PWM characterisation
Performed
PI control algorithm
Implemented in source
PI tuning and validation
Incomplete
Operating-mode definitions
Preliminary
State-machine structure
Preliminary
Valve integration
Incomplete
Unified firmware integration
Requires further work
