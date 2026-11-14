from machine import Pin, PWM

from config import (
    MOTOR_PWM_PIN,
    MOTOR_IN1_PIN,
    MOTOR_IN2_PIN,
    MOTOR_PWM_FREQUENCY
)


class Motor:
    """DC motor driver using an L298N-compatible interface."""

    def __init__(self, pwm_freq=MOTOR_PWM_FREQUENCY):

        if not isinstance(pwm_freq, int) or pwm_freq <= 0:
            raise ValueError("PWM frequency must be a positive integer")

        self.ena = PWM(Pin(MOTOR_PWM_PIN))
        self.ena.freq(pwm_freq)

        self.in1 = Pin(MOTOR_IN1_PIN, Pin.OUT)
        self.in2 = Pin(MOTOR_IN2_PIN, Pin.OUT)

        self.stop()

        print("Motor initialized")
        print("PWM frequency:", pwm_freq, "Hz")

    def forward(self):
        self.in1.value(1)
        self.in2.value(0)

    def reverse(self):
        self.in1.value(0)
        self.in2.value(1)

    def stop(self):
        self.ena.duty_u16(0)
        self.in1.value(0)
        self.in2.value(0)

    def set_speed(self, percent):
        """Set motor PWM duty cycle from 0 to 100 percent."""

        if not isinstance(percent, (int, float)):
            raise TypeError("PWM percentage must be numeric")

        if percent != percent:
            raise ValueError("PWM percentage cannot be NaN")

        percent = max(0.0, min(100.0, percent))
        duty = int(percent * 65535 / 100)

        self.ena.duty_u16(duty)
