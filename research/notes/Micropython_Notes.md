# MicroPython Notes

## Purpose

MicroPython provides a lightweight Python implementation for programming microcontrollers such as the Raspberry Pi Pico W.

---

## 1. `machine.Pin`

Represents a General Purpose Input/Output (GPIO) pin.

### Common Usage

```python
from machine import Pin

led = Pin(15, Pin.OUT)
led.on()
led.off()
led.toggle()
```

### Applications in this Project

* External status LED.
* Push button inputs.
* Solenoid valve control.
* Future status indicators.

---

## 2. `machine.PWM`

Used to generate Pulse Width Modulation signals.

### Common Usage

```python
from machine import Pin, PWM

pump = PWM(Pin(15))
pump.freq(1000)
pump.duty_u16(32768)
```

### Important Functions

* `PWM(Pin(x))` : create PWM object.
* `freq(f)` : set PWM frequency.
* `duty_u16(value)` : set duty cycle (0–65535).
* `deinit()` : disable PWM.

### Applications in this Project

* Control average power delivered to the KMDP-U1 vacuum pump.
* Future closed-loop control output from the PID controller.

---

## 3. `machine.I2C`

Implements the Inter-Integrated Circuit communication protocol.

### Common Usage

```python
from machine import Pin, I2C

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
print(i2c.scan())
```

### Key Functions

* `scan()`
* `readfrom()`
* `writeto()`
* `readfrom_mem()`
* `writeto_mem()`

### Applications in this Project

* Communication with BMP280 pressure sensor.
* Potential future OLED display integration.

---

## 4. `machine.PIO` (RP2040/RP2350 Feature)

Programmable I/O allows creation of custom hardware interfaces in software.

### Typical Applications

* WS2812 (NeoPixel) LEDs.
* Custom serial protocols.
* Precise timing applications.

### Relevance to this Project

Current proof-of-concept does not require PIO. Standard GPIO, PWM, and I²C peripherals are sufficient.

---

## Embedded Programming Pattern

Most embedded programs follow the same structure:

1. Import required modules.
2. Initialize hardware.
3. Configure peripherals.
4. Enter infinite control loop.
5. Read inputs → Process → Update outputs.

General pseudocode:

```
initialize_hardware()

while True:
    read_inputs()
    compute_control()
    update_outputs()
```

---

## Future Firmware Architecture

```
main.py
    │
    ├── drivers/
    │      └── bmp280.py
    │
    ├── control/
    │      ├── pump.py
    │      ├── valve.py
    │      └── pid.py
    │
    └── tests/
           ├── blink.py
           ├── pwm_test.py
           └── i2c_scan.py
```

The goal is to separate hardware drivers, control logic, and testing code into independent modules.
