import random
from time import sleep

pressure = 0

reference = -120

Kp = 1

Ki = 0.05
integral = 0

Kd = 0.2
previous_error = 0

leak_rate = 2

mode = "STIMULATION"
stim_mode = -120
expr_mode = -180
mode_switch_step = 20

for i in range(100):

    mode = "STIMULATION" if i < 20 else "EXPRESSION"
    reference = -120 if mode == "STIMULATION" else -180

    measured_pressure = pressure + random.uniform(-2,2)

    error = reference - measured_pressure

    integral += error

    derivative = error - previous_error
    previous_error = error

    if integral > 500:
        integral = 500
    if integral < -500:
        integral = -500

    control = Kp * (error) + Ki * (integral) + Kd*(derivative)
    pwm = -control

    if pwm > 100:
        pwm = 100
    if pwm < 0:
        pwm = 0

    pressure -= pwm * 0.1
    pressure += leak_rate

    if i > 30 and i < 35:
        pressure += 5

    if pressure < -250:
        pressure = -250
        pwm = 0

    print(f"Step={i}",
          f"Mode={mode}",
          f"Measured Pressure={measured_pressure:.1f}"
          f"Pressure={pressure:.1f}",
          f"PWM={pwm:.1f}",
          f"Error={error:.1f}")
    sleep(0.2)
