from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff

from pressure_sensor import PressureSensor
from motor import Motor

from config import (
    I2C_ID,
    I2C_SCL_PIN,
    I2C_SDA_PIN,
    I2C_FREQUENCY,
    MOTOR_PWM_FREQUENCY
)


# ============================================================
# TEST SETTINGS
# ============================================================

PWM_LEVELS = [40, 50, 60, 70, 80, 90, 100]

TEST_TIME = 30
STEADY_STATE_WINDOW = 10

ATMOSPHERE_TOLERANCE = 0.15
ATMOSPHERE_STABLE_SAMPLES = 10
ATMOSPHERE_RESET_TIMEOUT = 60

# Historical experimental cutoff only.
# NOT a validated safety limit.
MAX_TEST_VACUUM = -220.0

SAMPLE_INTERVAL = 0.1

FILTER_ALPHA = 0.85
CALIBRATION_SAMPLES = 30


# ============================================================
# HARDWARE INITIALIZATION
# ============================================================

motor = None


def initialize_hardware():

    global motor

    i2c = I2C(
        I2C_ID,
        scl=Pin(I2C_SCL_PIN),
        sda=Pin(I2C_SDA_PIN),
        freq=I2C_FREQUENCY
    )

    sensor = PressureSensor(
        i2c,
        alpha=FILTER_ALPHA
    )

    motor = Motor(
        pwm_freq=MOTOR_PWM_FREQUENCY
    )

    motor.stop()

    return sensor


# ============================================================
# ATMOSPHERIC RESET
# ============================================================

def wait_for_atmospheric_reset(sensor, atmosphere):

    print()
    print("MANUAL ACTION REQUIRED:")
    print("1. Open / vent the chamber.")
    print("2. Allow atmospheric air to enter.")
    print("3. Reseal the chamber.")
    print()

    print("Waiting for atmospheric reset...")

    stable_count = 0
    start_time = ticks_ms()

    while ticks_diff(
        ticks_ms(),
        start_time
    ) < ATMOSPHERE_RESET_TIMEOUT * 1000:

        absolute_pressure = sensor.read()

        vacuum = absolute_pressure - atmosphere

        print(
            "RESET VAC:",
            round(vacuum, 2),
            "mmHg"
        )

        if abs(vacuum) <= ATMOSPHERE_TOLERANCE:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= ATMOSPHERE_STABLE_SAMPLES:

            print("Atmospheric reset confirmed.")
            return

        sleep(SAMPLE_INTERVAL)

    raise RuntimeError(
        "Atmospheric reset timeout. Test aborted."
    )


# ============================================================
# SINGLE PWM CHARACTERIZATION
# ============================================================

def run_pwm_test(sensor, pwm, atmosphere):

    motor.stop()

    print()
    print("Preparing PWM:", pwm, "%")

    wait_for_atmospheric_reset(
        sensor,
        atmosphere
    )

    print("Starting in 3 seconds...")
    sleep(3)

    vacuum_sum = 0.0
    vacuum_min = 0.0

    sample_count = 0

    steady_state_sum = 0.0
    steady_state_count = 0

    start_time = ticks_ms()

    motor.forward()
    motor.set_speed(pwm)

    try:

        while ticks_diff(
            ticks_ms(),
            start_time
        ) < TEST_TIME * 1000:

            current_time = ticks_ms()

            elapsed = ticks_diff(
                current_time,
                start_time
            ) / 1000.0

            absolute_pressure = sensor.read()

            vacuum = absolute_pressure - atmosphere

            if vacuum <= MAX_TEST_VACUUM:
                raise RuntimeError(
                    "Historical test cutoff reached: "
                    + str(vacuum)
                    + " mmHg"
                )

            vacuum_sum += vacuum
            sample_count += 1

            if vacuum < vacuum_min:
                vacuum_min = vacuum

            if elapsed >= TEST_TIME - STEADY_STATE_WINDOW:

                steady_state_sum += vacuum
                steady_state_count += 1

            print(
                "TIME:", round(elapsed, 1), "s",
                "| PWM:", pwm, "%",
                "| ABS:", round(absolute_pressure, 2),
                "mmHg",
                "| VAC:", round(vacuum, 2),
                "mmHg"
            )

            sleep(SAMPLE_INTERVAL)

    finally:
        motor.stop()

    if sample_count == 0:
        raise RuntimeError("No valid measurement samples collected")

    average_vacuum = vacuum_sum / sample_count

    if steady_state_count > 0:
        steady_state_vacuum = (
            steady_state_sum / steady_state_count
        )
    else:
        steady_state_vacuum = None

    return (
        pwm,
        average_vacuum,
        steady_state_vacuum,
        vacuum_min
    )


# ============================================================
# APPLICATION
# ============================================================

def main():

    try:

        print()
        print("========================================")
        print("PWM - VACUUM CHARACTERIZATION TEST")
        print("========================================")

        sensor = initialize_hardware()

        print()
        print("Calibrating atmospheric pressure...")

        atmosphere = sensor.calibrate_atmosphere(
            samples=CALIBRATION_SAMPLES
        )

        print(
            "Atmospheric pressure:",
            round(atmosphere, 2),
            "mmHg"
        )

        results = []

        for pwm in PWM_LEVELS:

            result = run_pwm_test(
                sensor,
                pwm,
                atmosphere
            )

            results.append(result)

            print()
            print("PWM:", pwm, "% COMPLETE")
            print("Average vacuum:", round(result[1], 2))

            if result[2] is not None:
                print(
                    "Steady-state vacuum:",
                    round(result[2], 2)
                )

            print(
                "Maximum observed vacuum:",
                round(result[3], 2)
            )

        print()
        print("========================================")
        print("FINAL CHARACTERIZATION RESULTS")
        print("========================================")

        print("PWM | AVG VAC | STEADY VAC | MAX OBS VAC")

        for result in results:

            print(
                result[0],
                "|",
                round(result[1], 2),
                "|",
                (
                    round(result[2], 2)
                    if result[2] is not None
                    else "N/A"
                ),
                "|",
                round(result[3], 2)
            )

        print()
        print("CHARACTERIZATION COMPLETE")

    finally:

        if motor is not None:
            motor.stop()

        print("Motor stop command issued.")


if __name__ == "__main__":
    main()
