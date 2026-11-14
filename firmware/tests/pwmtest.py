# LEGACY DIAGNOSTIC
# Historical GP15 PWM/LED experiment.
# Not part of the active Pico 2W motor-control firmware.
# Active motor interface: GP2 (PWM), GP3 (IN1), GP4 (IN2).
# Retained for project history; do not use as the current motor test.
#pwmtest.py

from time import sleep
from pump import Pump

pump = Pump(pin=15)

while True:

    print("25%")
    pump.set_speed(25)
    sleep(3)

    print("50%")
    pump.set_speed(50)
    sleep(3)

    print("75%")
    pump.set_speed(75)
    sleep(3)

    print("100%")
    pump.set_speed(100)
    sleep(3)

    print("STOP")
    pump.stop()
    sleep(3)
