from machine import Pin, PWM


class Motor:

    def __init__(self):

        # PWM pin
        self.ena = PWM(Pin(2))

        # Working PWM frequency
        self.ena.freq(1000)

        # Direction pins
        self.in1 = Pin(3, Pin.OUT)
        self.in2 = Pin(4, Pin.OUT)

        self.stop()

        print("Motor initialized")
        print("PWM frequency: 1000 Hz")


    def forward(self):

        self.in1.value(1)
        self.in2.value(0)

        print("Motor direction: FORWARD")


    def reverse(self):

        self.in1.value(0)
        self.in2.value(1)

        print("Motor direction: REVERSE")


    def stop(self):

        self.in1.value(0)
        self.in2.value(0)

        self.ena.duty_u16(0)

        print("Motor stopped")


    def set_speed(self, percent):

        percent = max(
            0,
            min(
                100,
                percent
            )
        )

        duty = int(
            percent
            *
            65535
            /
            100
        )

        self.ena.duty_u16(
            duty
        )
