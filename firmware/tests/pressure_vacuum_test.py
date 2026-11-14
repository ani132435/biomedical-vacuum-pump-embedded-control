from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff

from pressure_sensor import PressureSensor
from motor import Motor


# ============================================================
# SETTINGS
# ============================================================

PWM_LEVELS = [
    40,
    50,
    60,
    70,
    80,
    90,
    100
]

TEST_TIME = 30                  # seconds per PWM level

STEADY_STATE_WINDOW = 10        # final 10 seconds

ATMOSPHERE_TOLERANCE = 0.15     # mmHg

MAX_TEST_VACUUM = -220          # mmHg emergency cutoff

SAMPLE_INTERVAL = 0.1           # seconds


# ============================================================
# I2C SETUP
# ============================================================

i2c = I2C(
    0,
    scl=Pin(1),
    sda=Pin(0),
    freq=400000
)


# ============================================================
# PRESSURE SENSOR
# ============================================================

print()
print("Creating pressure sensor...")

sensor = PressureSensor(
    i2c,
    alpha=0.85
)

print("Pressure sensor ready")


# ============================================================
# MOTOR
# ============================================================

motor = Motor()

motor.stop()


# ============================================================
# TEST HEADER
# ============================================================

print()
print("========================================")
print("PWM - VACUUM CHARACTERIZATION TEST")
print("========================================")
print()

print("PWM levels:")
print(PWM_LEVELS)

print()
print("Test time:", TEST_TIME, "seconds")
print(
    "Steady-state window:",
    STEADY_STATE_WINDOW,
    "seconds"
)

print()


# ============================================================
# ATMOSPHERIC CALIBRATION
# ============================================================

print("IMPORTANT:")
print("Pump must be OFF.")
print("Chamber must be at atmospheric pressure.")
print()

print("Calibrating atmospheric pressure...")
print()


atmosphere = sensor.calibrate_atmosphere(
    samples=30
)


print()
print("========================================")
print("CALIBRATION COMPLETE")
print("========================================")

print(
    "Atmospheric pressure:",
    round(atmosphere, 2),
    "mmHg"
)

print()


# ============================================================
# RESULTS STORAGE
# ============================================================

results = []


# ============================================================
# TEST LOOP
# ============================================================

try:

    for pwm in PWM_LEVELS:


        # ====================================================
        # STOP MOTOR
        # ====================================================

        motor.stop()


        print()
        print("========================================")
        print("PREPARING PWM:", pwm, "%")
        print("========================================")

        print()
        print("MANUAL ACTION REQUIRED:")
        print("1. Open / vent the chamber.")
        print("2. Allow atmospheric air to enter.")
        print("3. Reseal the chamber.")
        print()

        print(
            "Waiting for vacuum to return near 0 mmHg..."
        )


        # ====================================================
        # ATMOSPHERIC RESET VERIFICATION
        # ====================================================

        stable_count = 0


        while True:

            absolute_pressure = sensor.read()


            vacuum = (
                absolute_pressure
                -
                atmosphere
            )


            print(
                "RESET VAC:",
                round(vacuum, 2),
                "mmHg"
            )


            if abs(vacuum) <= ATMOSPHERE_TOLERANCE:

                stable_count += 1

            else:

                stable_count = 0


            # Require 10 consecutive stable readings

            if stable_count >= 10:

                break


            sleep(SAMPLE_INTERVAL)


        print()
        print("Atmospheric reset confirmed.")

        print(
            "Starting",
            pwm,
            "% PWM test in 3 seconds..."
        )

        sleep(3)


        # ====================================================
        # START MOTOR
        # ====================================================

        motor.forward()

        motor.set_speed(pwm)


        print()
        print("========================================")
        print("TESTING PWM:", pwm, "%")
        print("========================================")
        print()


        # ====================================================
        # MEASUREMENT VARIABLES
        # ====================================================

        vacuum_sum = 0.0

        vacuum_min = 0.0

        sample_count = 0


        steady_state_sum = 0.0

        steady_state_count = 0


        start_time = ticks_ms()


        # ====================================================
        # MEASUREMENT LOOP
        # ====================================================

        while ticks_diff(
            ticks_ms(),
            start_time
        ) < TEST_TIME * 1000:


            current_time = ticks_ms()


            elapsed = (
                ticks_diff(
                    current_time,
                    start_time
                )
                /
                1000
            )


            # ------------------------------------------------
            # PRESSURE
            # ------------------------------------------------

            absolute_pressure = sensor.read()


            vacuum = (
                absolute_pressure
                -
                atmosphere
            )


            # ------------------------------------------------
            # SAFETY CUTOFF
            # ------------------------------------------------

            if vacuum <= MAX_TEST_VACUUM:

                motor.stop()


                print()
                print("!!! VACUUM LIMIT REACHED !!!")


                print(
                    "Measured vacuum:",
                    round(vacuum, 2),
                    "mmHg"
                )


                raise RuntimeError(
                    "Vacuum safety cutoff"
                )


            # ------------------------------------------------
            # OVERALL DATA
            # ------------------------------------------------

            vacuum_sum += vacuum

            sample_count += 1


            if vacuum < vacuum_min:

                vacuum_min = vacuum


            # ------------------------------------------------
            # STEADY-STATE DATA
            # FINAL 10 SECONDS
            # ------------------------------------------------

            if elapsed >= (
                TEST_TIME
                -
                STEADY_STATE_WINDOW
            ):

                steady_state_sum += vacuum

                steady_state_count += 1


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            print(
                "TIME:",
                round(elapsed, 1),
                "s",
                "| PWM:",
                pwm,
                "%",
                "| ABS:",
                round(absolute_pressure, 2),
                "mmHg",
                "| VAC:",
                round(vacuum, 2),
                "mmHg"
            )


            sleep(SAMPLE_INTERVAL)


        # ====================================================
        # STOP MOTOR
        # ====================================================

        motor.stop()


        # ====================================================
        # CALCULATE RESULTS
        # ====================================================

        average_vacuum = (
            vacuum_sum
            /
            sample_count
        )


        if steady_state_count > 0:

            steady_state_vacuum = (
                steady_state_sum
                /
                steady_state_count
            )

        else:

            steady_state_vacuum = 0


        # ====================================================
        # STORE RESULTS
        # ====================================================

        results.append(
            (
                pwm,
                average_vacuum,
                steady_state_vacuum,
                vacuum_min
            )
        )


        # ====================================================
        # PWM RESULT
        # ====================================================

        print()
        print("========================================")

        print(
            "PWM",
            pwm,
            "% COMPLETE"
        )

        print("========================================")


        print(
            "Overall average vacuum:",
            round(average_vacuum, 2),
            "mmHg"
        )


        print(
            "Steady-state vacuum:",
            round(steady_state_vacuum, 2),
            "mmHg"
        )


        print(
            "Maximum observed vacuum:",
            round(vacuum_min, 2),
            "mmHg"
        )


        print()


    # ========================================================
    # ALL TESTS COMPLETE
    # ========================================================

    motor.stop()


    print()
    print("========================================")
    print("FINAL PWM - VACUUM RESULTS")
    print("========================================")

    print()

    print(
        "PWM | AVG VAC | STEADY VAC | MAX OBS VAC"
    )

    print(
        "-----------------------------------------"
    )


    for result in results:

        pwm = result[0]

        average = result[1]

        steady = result[2]

        maximum = result[3]


        print(
            pwm,
            "|",
            round(average, 2),
            "|",
            round(steady, 2),
            "|",
            round(maximum, 2)
        )


    print()
    print("CHARACTERIZATION COMPLETE")
    print("Pump stopped")


# ============================================================
# KEYBOARD STOP
# ============================================================

except KeyboardInterrupt:

    motor.stop()

    print()
    print("TEST MANUALLY STOPPED")
    print("Pump stopped")


# ============================================================
# ERROR STOP
# ============================================================

except Exception as error:

    motor.stop()

    print()
    print("TEST STOPPED DUE TO ERROR")

    print(
        "Error:",
        error
    )
