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
