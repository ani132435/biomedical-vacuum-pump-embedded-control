# System Architecture

## Embedded Architecture

```text
Raspberry Pi Pico 2W
 │
 ├── I²C ─────► BMP280 Pressure Sensor
 │
 ├── PWM ─────► L298N Motor Driver
 │                   │
 │                   ▼
 │             KMDP 24V Pump
 │
 ├── GPIO ────► Valve Driver
 │                   │
 │                   ▼
 │          CKS5001/04 Solenoid Valve
 │
 ├── GPIO ◄── Push Buttons
 │
 └── USB/UART ─► Laptop (Debug/Data Logging)
```

---

## Pneumatic Architecture

```text
KMDP Pump
     │
     ▼
CKS5001/04 Valve
     │
     ▼
Niscomed Flange
     │
     ▼
Breast Chamber
     │
     ├── Pressure Tap
     │        │
     │        ▼
     │     BMP280
     │
     ▼
Milk Collection Bottle
```

---

## Future Integration

- OLED display.
- Breast milk analyser module.
- Wireless data logging.