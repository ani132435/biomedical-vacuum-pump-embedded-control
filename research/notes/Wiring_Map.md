# Pin Assignments and Wiring Map

## Microcontroller

* **Board:** Raspberry Pi Pico W
* **Firmware:** MicroPython
* **Development Interface:** USB + Thonny

---

# GPIO Assignment Table

| Pico Pin | GPIO   | Function                        | Connected To                        | Status      |
| -------- | ------ | ------------------------------- | ----------------------------------- | ----------- |
| GP0      | GPIO0  | I²C SDA                         | BMP280 SDA                          | Planned     |
| GP1      | GPIO1  | I²C SCL                         | BMP280 SCL                          | Planned     |
| GP2      | GPIO2  | Push Button 1                   | Mode Select                         | Reserved    |
| GP3      | GPIO3  | Push Button 2                   | Start / Stop                        | Reserved    |
| GP15     | GPIO15 | PWM Output                      | L298N ENA (Pump Speed Control)      | Planned     |
| GP16     | GPIO16 | Digital Output                  | Solenoid Valve Driver (MOSFET Gate) | Planned     |
| 3V3(OUT) | —      | 3.3 V Supply                    | BMP280 VCC                          | Planned     |
| VSYS     | —      | External Power Input (optional) | 3.7 V Battery (future)              | Reserved    |
| GND      | —      | Common Ground                   | Shared by all modules               | Implemented |
| USB      | —      | Development Power + Programming | Laptop USB                          | Implemented |

---

# Power Architecture

## Development Mode

Laptop USB
→ Raspberry Pi Pico W

18650 Battery
→ XL6009 Boost Converter
→ 24 V Rail
→ L298N
→ KMDP-U1 Pump

**Important:** USB and battery grounds are connected together (common GND).

---

# Pump Driver Connections (L298N)

| L298N Pin  | Connected To                    |
| ---------- | ------------------------------- |
| ENA        | GP15 (PWM)                      |
| IN1        | 3.3 V or GPIO (direction fixed) |
| IN2        | GND or GPIO (direction fixed)   |
| OUT1       | KMDP Pump Terminal 1            |
| OUT2       | KMDP Pump Terminal 2            |
| +12V / VIN | XL6009 24 V Output              |
| GND        | Common Ground                   |

**Note:** Current proof-of-concept uses L298N. Future versions may replace it with a logic-level MOSFET driver.

---

# BMP280 Connections

| BMP280 Pin | Pico Connection |
| ---------- | --------------- |
| VCC        | 3V3(OUT)        |
| GND        | GND             |
| SDA        | GP0             |
| SCL        | GP1             |

I²C Bus:

* SDA → GP0
* SCL → GP1

---

# Solenoid Valve Connections (Planned)

The CKS5001/04 valve should NOT be driven directly from a GPIO pin.

Proposed interface:

GP16
→ Gate resistor (~220 Ω)
→ Logic-level N-MOSFET Gate

MOSFET Drain
→ Solenoid Valve Negative

Solenoid Valve Positive
→ +5 V Supply

MOSFET Source
→ Common GND

A flyback diode should be connected across the valve terminals.

---

# Push Buttons

| Button   | Pico GPIO | Function     |
| -------- | --------- | ------------ |
| Button 1 | GP2       | Mode Select  |
| Button 2 | GP3       | Start / Stop |

Internal pull-up resistors may be enabled in software using `Pin.PULL_UP`.

---

# Firmware Module Mapping

| Firmware File    | Hardware Controlled          |
| ---------------- | ---------------------------- |
| `blink.py`       | External LED                 |
| `gpio_test.py`   | Generic GPIO Output          |
| `pwm_test.py`    | PWM Generator                |
| `i2c_scan.py`    | I²C Bus Detection            |
| `bmp280_test.py` | BMP280 Pressure Sensor       |
| `pump.py`        | KMDP-U1 Pump                 |
| `valve.py`       | CKS5001/04 Solenoid Valve    |
| `pid.py`         | Closed-loop Pressure Control |

---

# Overall System Architecture

```text
          USB
           │
           ▼
   Raspberry Pi Pico W
           │
   ┌───────┼───────────┐
   │       │           │
   ▼       ▼           ▼
 BMP280  Buttons   PWM (GP15)
   │                   │
   │                   ▼
   │               L298N Driver
   │                   │
   │                   ▼
   │              KMDP-U1 Pump
   │
   └──────── Feedback ───────┐
                             │
                    Pneumatic Chamber
                             │
                             ▼
                     Solenoid Valve
                             │
                             ▼
                    Breast Flange Assembly
```

## Notes

* The Pi Pico W acts as the system controller.
* The KMDP-U1 pump is the actuator.
* The BMP280 is the feedback sensor.
* The CKS5001/04 valve provides pneumatic flow control.
* Closed-loop control will adjust PWM duty cycle based on measured chamber pressure.
