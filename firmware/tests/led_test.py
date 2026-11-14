from machine import Pin
from time import sleep

p = Pin(15, Pin.OUT)

print("LED is flashing...")

while True:
    p.value(1)
    sleep(1)
    p.value(0)
    sleep(1)
