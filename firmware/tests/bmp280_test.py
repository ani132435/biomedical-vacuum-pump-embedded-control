# bmp280_test.py

from machine import Pin, I2C
from bmp280 import BMP280
from time import sleep

i2c = I2C(
    0,
    scl=Pin(1),
    sda=Pin(0),
    freq=100000
)

bmp = BMP280(i2c)

while True:
    print("Pressure:", bmp.pressure)
    print("----------------")
    sleep(1)
