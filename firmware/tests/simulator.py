from time import sleep

pressure = 0

reference = -120

Kp = 0.5

Ki = 0.01
integral = 0

leak_rate = 2

mode = "STIMULATION"
stim_mode = -120
expr_mode = -180
mode_switch_step = 20

for i in range(100):

    if i == mode_switch_step:
        mode = "EXPRESSION"

    reference = stim_mode if mode == "STIMULATION" else expr_mode

    error = reference - pressure

    integral += error

    if i == 40:
        leak_rate = 6


    if integral > 500:
        integral = 500

    if integral < -500:
        integral = -500

    pwm = Kp * (-error) + Ki * (-integral)

    if pwm > 100:
        pwm = 100

    if pwm < 0:
        pwm = 0

    pressure -= pwm * 0.5

    pressure += leak_rate

    if pressure < -250:
        pressure = -250
        pwm = 0

    print(
        f"Step={i}",
        f"Pressure={pressure:.1f}",
        f"PWM={pwm:.1f}",
        f"Error={error:.1f}"
    )

    sleep(0.2)
