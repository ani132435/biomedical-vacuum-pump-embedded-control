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
