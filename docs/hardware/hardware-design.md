Hardware Design
1. Overview
The hardware development focused on assembling and testing a
pressure-monitored vacuum-pump prototype.
The system development involved a microcontroller, pressure
sensor, motor driver, DC vacuum pump and pneumatic components.
2. Main Components
Component
Model
Function
Microcontroller
Raspberry Pi Pico 2W
Embedded control
Pressure sensor
BMP280
Absolute pressure measurement
Motor driver
L298N
DC motor actuation
Vacuum pump
KMDP-U1-24V
Vacuum generation
Solenoid valve
CKS5001/04
Intended pneumatic switching
DC-DC converter
XL6009
Power conversion during development
This list represents components documented during development.
It does not imply that all components were used simultaneously
in every experiment.
3. KMDP-U1-24V Vacuum Pump
The pump was measured on 16 June 2025 for mechanical
reverse engineering and CAD modelling.
Parameter
Recorded value
Rated voltage
24 V
Power
12 W
Flow rate
10 L/min
Stated maximum vacuum
-70 kPa
Overall length
80 mm
Overall width
50 mm
Overall height
105 mm
Motor diameter
55 mm
Motor length
60 mm
Hose port outer diameter
12 mm
Hose port inner diameter
4 mm
The vacuum and flow values are recorded component specifications,
not measured performance values from the prototype experiments.
4. BMP280 Pressure Sensor
The BMP280 was interfaced with the Pico 2W using I2C.
Parameter
Configuration
I2C controller
I2C(0)
SDA
GP0
SCL
GP1
Bus frequency
400 kHz
Address used in one driver variant
0x76
The sensor measures absolute pressure. Gauge pressure is obtained
by subtracting the atmospheric reference.
5. Motor Driver
The L298N module was used for DC pump actuation.
The inspected motor firmware assigns:
- GP2 to the PWM signal.
- GP3 to direction input 1.
- GP4 to direction input 2.
- 1 kHz PWM frequency.
The motor software provides forward, reverse, stop and speed
control functions.
The exact power wiring and supply arrangement should be checked
against the physical prototype before circuit reproduction.
6. Solenoid Valve
The CKS5001/04 valve was measured for mechanical modelling.
Parameter
Recorded value
Operating voltage
5 V DC
Configuration
Two-wire solenoid
Body length
14 mm
Body width
13 mm
Body height
20 mm
Front port outer diameter
7 mm
Front port inner diameter
3 mm
The valve-control software is preliminary. Its complete
electrical driver and pneumatic integration were not validated.
7. Mechanical Design
FreeCAD was used to develop models for:
- KMDP pump motor sleeve.
- CKS5001/04 solenoid valve.
The corresponding FreeCAD project files are included in the
repository. The models document mechanical design work and
reverse engineering; fabricated and mechanically validated
parts are not claimed.
8. KiCad Design
A KiCad schematic project is included as an earlier ESP32-based
design reference.
The later prototype development used the Raspberry Pi Pico 2W.
Therefore, the schematic should not be interpreted as the final
as-built Pico 2W wiring diagram.
9. Hardware Limitations
- The intended pressure range was not achieved.
- Valve integration was incomplete.
- CAD models were not validated through fabricated components.
- The KiCad schematic represents an earlier design iteration.
- The complete power-distribution arrangement requires
- verification against the physical prototype.
