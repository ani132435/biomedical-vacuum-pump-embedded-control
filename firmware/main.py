from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff

from pressure_sensor import PressureSensor
from motor import Motor
from controller import PIController

from config import (
    I2C_ID,
    I2C_SCL_PIN,
    I2C_SDA_PIN,
    I2C_FREQUENCY,
    MOTOR_PWM_FREQUENCY,
    TARGET_VACUUM,
    BASE_PWM,
    MIN_PWM,
    MAX_PWM,
    KP,
    KI,
    CONTROL_INTERVAL,
    TEST_TIME,
    PRESSURE_FILTER_ALPHA,
    ATMOSPHERE_CALIBRATION_SAMPLES
)


# ============================================================
# CONTROL APPLICATION
# ============================================================

def run_control(sensor, motor, controller):

    print()
    print("========================================")
    print("CLOSED LOOP PI VACUUM CONTROL")
    print("========================================")

    print("Target:", TARGET_VACUUM, "mmHg")
    print("Kp:", KP)
    print("Ki:", KI)
    print("Base PWM:", BASE_PWM, "%")
    print("PWM limits:", MIN_PWM, "-", MAX_PWM, "%")

    motor.stop()

    print()
    print("Calibrating atmospheric pressure...")

    atmosphere = sensor.calibrate_atmosphere(
        samples=ATMOSPHERE_CALIBRATION_SAMPLES
    )

    print(
        "Atmospheric pressure:",
        round(atmosphere, 2),
        "mmHg"
    )

    controller.reset()
    motor.forward()

    start_time = ticks_ms()
    previous_time = start_time

    print()
    print("Starting closed-loop control...")

    while ticks_diff(ticks_ms(), start_time) < TEST_TIME * 1000:

        current_time = ticks_ms()
        dt_ms = ticks_diff(current_time, previous_time)

        if dt_ms <= 0:
            sleep(0.001)
            continue

        dt = dt_ms / 1000.0
        previous_time = current_time

        vacuum = sensor.vacuum()
        error = vacuum - TARGET_VACUUM

        correction = controller.update(error, dt)

        pwm = BASE_PWM + correction
        pwm = max(MIN_PWM, min(MAX_PWM, pwm))

        motor.set_speed(pwm)

        elapsed = ticks_diff(
            current_time,
            start_time
        ) / 1000.0

        print(
            "TIME:", round(elapsed, 1), "s",
            "| VAC:", round(vacuum, 2), "mmHg",
            "| TARGET:", TARGET_VACUUM,
            "| ERROR:", round(error, 2),
            "| PWM:", round(pwm, 1), "%",
            "| INT:", round(controller.integral, 2)
        )

        sleep(CONTROL_INTERVAL)

    print()
    print("Closed-loop test completed.")


# ============================================================
# APPLICATION INITIALIZATION AND EXECUTION
# ============================================================

def main():

    motor = None

    try:
        print("Initializing I2C...")

        i2c = I2C(
            I2C_ID,
            scl=Pin(I2C_SCL_PIN),
            sda=Pin(I2C_SDA_PIN),
            freq=I2C_FREQUENCY
        )

        print("Initializing pressure sensor...")

        sensor = PressureSensor(
            i2c,
            alpha=PRESSURE_FILTER_ALPHA
        )

        print("Initializing motor...")

        motor = Motor(pwm_freq=MOTOR_PWM_FREQUENCY)

        controller = PIController(
            kp=KP,
            ki=KI,
            output_min=MIN_PWM - BASE_PWM,
            output_max=MAX_PWM - BASE_PWM
        )

        run_control(sensor, motor, controller)

    except KeyboardInterrupt:
        print()
        print("Control interrupted by user.")

    except Exception as exc:
        print()
        print("CONTROL APPLICATION ERROR:")
        print(exc)

    finally:
        if motor is not None:
            motor.stop()
            print("Motor stopped.")


if __name__ == "__main__":
    main()
