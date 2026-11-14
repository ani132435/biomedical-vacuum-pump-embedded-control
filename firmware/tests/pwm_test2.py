# LEGACY DIAGNOSTIC
# Historical GP15 PWM/LED experiment.
# Not part of the active Pico 2W motor-control firmware.
# Active motor interface: GP2 (PWM), GP3 (IN1), GP4 (IN2).
# Retained for project history; do not use as the current motor test.
from machine import PWM, Pin
from time import sleep

led = PWM(Pin(15))
led.freq(1000)

while True:
    led.duty_u16(10000)
    sleep(1)

    led.duty_u16(30000)
    sleep(1)

    led.duty_u16(50000)
    sleep(1)

    led.duty_u16(65000)
    sleep(1)

    led.duty_u16(0)
    sleep(1)
