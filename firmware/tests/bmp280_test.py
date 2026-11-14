from machine import Pin, I2C
from time import sleep
from bmp280_sensor import BMP280

i2c = I2C(
    0,
    scl=Pin(1),
    sda=Pin(0),
    freq=400000
)

print("Scanning I2C...")
print("Devices:", i2c.scan())

bmp = BMP280(i2c)

print("BMP280 initialised.")

for index in range(10):
    data = bmp.read()

    if data is None:
        print("Sample:", index + 1, "| Invalid sensor reading")
    else:
        print(
            "Sample:", index + 1,
            "| Pressure:", round(data["pressure_mmhg"], 2), "mmHg",
            "| Temperature:", round(data["temperature"], 2), "C"
        )

    sleep(1)

print("Sensor diagnostic complete.")
