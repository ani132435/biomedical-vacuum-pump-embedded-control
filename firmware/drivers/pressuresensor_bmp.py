from machine import Pin, I2C
from time import sleep_ms
import struct


i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=10000)
ADDR = 0x76

# Dummy read
try: i2c.readfrom_mem(ADDR, 0xD0, 1)
except: pass
sleep_ms(10)

# Wake sensor
i2c.writeto(ADDR, bytes([0xF4, 0x27]))
sleep_ms(100)

# Calibration constants
T1 = 28184
T2 = 26430
T3 = 50
P1 = 37994
P2 = -10689
P3 = 3024
P4 = 8730
P5 = 122
P6 = -7
P7 = 9900
P8 = -10230
P9 = 4285

def compensate(raw_bytes):
    # Parse raw pressure and temperature
    raw_p = (raw_bytes[0] << 12) | (raw_bytes[1] << 4) | (raw_bytes[2] >> 4)
    raw_t = (raw_bytes[3] << 12) | (raw_bytes[4] << 4) | (raw_bytes[5] >> 4)

    # Temperature compensation (Bosch formula)
    var1 = (raw_t / 16384.0 - T1 / 1024.0) * T2
    var2 = (raw_t / 131072.0 - T1 / 8388608.0) ** 2 * T3
    t_fine = var1 + var2
    temp_c = t_fine / 5120.0

    # Pressure compensation (Bosch formula)
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * P6 / 32768.0
    var2 = var2 + var1 * P5 * 2.0
    var2 = var2 / 4.0 + P4 * 65536.0
    var1 = (P3 * var1 * var1 / 524288.0 + P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * P1

    # Avoid division by zero
    if var1 == 0:
        return None, temp_c

    pressure = 1048576.0 - raw_p
    pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
    var1 = P9 * pressure * pressure / 2147483648.0
    var2 = pressure * P8 / 32768.0
    pressure = pressure + (var1 + var2 + P7) / 16.0

    # Convert Pa → hPa → mmHg
    pressure_hpa = pressure / 100.0
    pressure_mmhg = pressure_hpa * 0.75006

    return pressure_hpa, pressure_mmhg, temp_c

# Read loop
print("Reading pressure and temperature...\n")
for _ in range(10):
    raw = i2c.readfrom_mem(ADDR, 0xF7, 6)
    result = compensate(raw)
    if result:
        hpa, mmhg, temp = result
        print(f"Pressure: {hpa:.2f} hPa | {mmhg:.2f} mmHg | Temp: {temp:.2f} C")
    sleep_ms(1000)
