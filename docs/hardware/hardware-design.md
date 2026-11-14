# Hardware Design

## 1. Overview

The hardware development focused on assembling and testing a pressure-monitored vacuum-pump prototype. The system evolved through multiple development iterations involving a microcontroller, pressure sensor, motor driver, DC vacuum pump, power-conversion components, and pneumatic components.

This document records the components and interfaces identified during development. It is not a final, verified wiring or manufacturing specification.

## 2. Main Components

| Component | Model | Role |
|---|---|---|
| Microcontroller | Raspberry Pi Pico 2W | Later embedded controller |
| Pressure sensor | BMP280 | Absolute-pressure measurement |
| Motor driver | L298N | DC motor actuation |
| Vacuum pump | KMDP-U1-24V | Vacuum generation |
| Solenoid valve | CKS5001/04 | Intended pneumatic switching; integration incomplete |
| DC-DC converter | XL6009 | Power conversion used during development |

These components were documented across development. They were not necessarily used simultaneously in every experiment.

## 3. KMDP-U1-24V Vacuum Pump

The pump was measured on 16 June 2025 for mechanical reverse engineering and CAD modelling.

| Parameter | Recorded value |
|---|---:|
| Rated voltage | 24 V |
| Rated power | 12 W |
| Stated flow rate | 10 L/min |
| Stated maximum vacuum | -70 kPa |
| Overall length | 80 mm |
| Overall width | 50 mm |
| Overall height | 105 mm |
| Motor diameter | 55 mm |
| Motor length | 60 mm |
| Hose-port outer diameter | 12 mm |
| Hose-port inner diameter | 4 mm |

**Important:** The flow and maximum-vacuum values are recorded component specifications, not measured prototype performance.

## 4. BMP280 Pressure Sensor

The BMP280 was interfaced with the Raspberry Pi Pico 2W over I2C during later development.

| Parameter | Configuration |
|---|---|
| I2C controller | `I2C(0)` |
| SDA | GP0 |
| SCL | GP1 |
| Bus frequency | 400 kHz |
| Address used in one driver variant | `0x76` |

The BMP280 measures absolute pressure. Gauge pressure is calculated relative to atmospheric pressure:

`P_gauge = P_absolute - P_atmospheric`

The atmospheric reference and sensor calibration procedure must be checked when repeating measurements. Different driver versions may configure the sensor differently.

## 5. Motor Driver and Firmware Pin Assignment

The L298N module was used for DC pump actuation. The inspected motor firmware assigns the following Pico 2W GPIO pins:

| Signal | Pico 2W pin |
|---|---|
| PWM speed command | GP2 |
| Direction input 1 | GP3 |
| Direction input 2 | GP4 |
| PWM frequency | 1 kHz |

The motor software includes forward, reverse, stop, and speed-control functions.

These are firmware signal assignments, not a complete wiring diagram. Verify the actual motor-driver module, motor supply, logic supply, common-ground arrangement, enable-pin wiring, and protection components against the physical hardware before reproducing the circuit.

## 6. Solenoid Valve

The CKS5001/04 valve was measured for mechanical modelling.

| Parameter | Recorded value |
|---|---:|
| Operating voltage | 5 V DC |
| Configuration | Two-wire solenoid |
| Body length | 14 mm |
| Body width | 13 mm |
| Body height | 20 mm |
| Front-port outer diameter | 7 mm |
| Front-port inner diameter | 3 mm |

The valve-control software is preliminary. Its complete electrical driver, power stage, and pneumatic integration were not validated.

## 7. Mechanical Design

FreeCAD was used to develop preliminary models for:

- The KMDP pump motor sleeve.
- The CKS5001/04 solenoid valve.

The corresponding FreeCAD project files and measurement references are included in the repository. The models document measurement and CAD work; they should not be interpreted as fabricated or mechanically validated components.

## 8. KiCad Design Reference

A KiCad schematic project is included as an earlier ESP32-based design reference.

Later prototype development used the Raspberry Pi Pico 2W. Therefore, the ESP32 schematic must **not** be treated as the final as-built Pico 2W wiring diagram.

## 9. Hardware Limitations

- The intended pressure range was not achieved in the recorded prototype experiments.
- Solenoid-valve electrical and pneumatic integration remained incomplete.
- CAD models were not validated through fabrication and fit testing.
- The KiCad schematic represents an earlier ESP32-based design iteration.
- A complete, verified power-distribution and wiring diagram remains to be established.
- Component specifications must not be substituted for measured system performance.

## 10. Related Documentation

- [System Architecture](../architecture/system-architecture.md)
- [Firmware Documentation](../firmware/firmware-documentation.md)
- [Project Status and Future Work](../project-status.md)
- [Experimental Methodology](../experiments/experimental-methodology.md)
- [Results and Analysis](../experiments/results-and-analysis.md)
