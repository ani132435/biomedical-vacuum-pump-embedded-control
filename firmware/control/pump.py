from machine import Pin, PWM

class Pump:

    def __init__(self, pin, freq=1000):

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)

        self.stop()

    def set_speed(self, percent):

        percent = max(0, min(100, percent))

        duty = int(percent * 65535 / 100)

        self.pwm.duty_u16(duty)

    def stop(self):

        self.pwm.duty_u16(0)
