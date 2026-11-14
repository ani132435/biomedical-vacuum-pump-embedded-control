from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff

from pressure_sensor import PressureSensor
from motor import Motor
from controller import PIController


# ============================================================
# CONTROL SETTINGS
# ============================================================

TARGET_VACUUM = -2.5      # mmHg

BASE_PWM = 60             # %

MIN_PWM = 40              # Motor operating threshold
MAX_PWM = 80              # Stable tested PWM limit

KP = 8.0
KI = 1.0

CONTROL_INTERVAL = 0.1    # seconds

TEST_TIME = 30            # seconds


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
# PI CONTROLLER
# ============================================================

controller = PIController(
    kp=KP,
    ki=KI
)

controller.reset()


# ============================================================
# TEST INFORMATION
# ============================================================

print()
print("========================================")
print("CLOSED LOOP PI VACUUM CONTROL")
print("========================================")

print()
print(
    "Target vacuum:",
    TARGET_VACUUM,
    "mmHg"
)

print(
    "Kp:",
    KP
)

print(
    "Ki:",
    KI
)

print(
    "Base PWM:",
    BASE_PWM,
    "%"
)

print()


# ============================================================
# ATMOSPHERIC CALIBRATION
# ============================================================

print("Keep pump OFF.")
print("Calibrating atmospheric pressure...")

atmosphere = sensor.calibrate_atmosphere(
    samples=30
)

print()
print(
    "Atmospheric pressure:",
    round(
        atmosphere,
        2
    ),
    "mmHg"
)

print()


# ============================================================
# RESET CONTROLLER
# ============================================================

controller.reset()


# ============================================================
# START MOTOR DIRECTION
# ============================================================

motor.forward()


# ============================================================
# CONTROL TIMING
# ============================================================

start_time = ticks_ms()

previous_time = ticks_ms()


# ============================================================
# CLOSED LOOP CONTROL
# ============================================================

try:

    while ticks_diff(
        ticks_ms(),
        start_time
    ) < TEST_TIME * 1000:


        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        current_time = ticks_ms()


        dt = (
            ticks_diff(
                current_time,
                previous_time
            )
            /
            1000
        )


        previous_time = current_time


        # ----------------------------------------------------
        # PRESSURE SENSOR FEEDBACK
        # ----------------------------------------------------

        absolute_pressure = sensor.read()


        vacuum = (
            absolute_pressure
            -
            atmosphere
        )


        # ----------------------------------------------------
        # ERROR CALCULATION
        # ----------------------------------------------------

        error = (
            vacuum
            -
            TARGET_VACUUM
        )


        # ----------------------------------------------------
        # PI CONTROLLER
        # ----------------------------------------------------

        correction = controller.update(
            error,
            dt
        )


        # ----------------------------------------------------
        # CONTROL OUTPUT
        # ----------------------------------------------------

        pwm = (
            BASE_PWM
            +
            correction
        )


        # ----------------------------------------------------
        # PWM UPPER AND LOWER LIMIT
        # ----------------------------------------------------

        pwm = max(
            0,
            min(
                MAX_PWM,
                pwm
            )
        )


        # ----------------------------------------------------
        # MOTOR DEAD ZONE
        # ----------------------------------------------------

        if (
            pwm > 0
            and
            pwm < MIN_PWM
        ):

            pwm = MIN_PWM


        # ----------------------------------------------------
        # APPLY MOTOR COMMAND
        # ----------------------------------------------------

        motor.set_speed(
            pwm
        )


        # ----------------------------------------------------
        # ELAPSED TIME
        # ----------------------------------------------------

        elapsed = (
            ticks_diff(
                current_time,
                start_time
            )
            /
            1000
        )


        # ----------------------------------------------------
        # DISPLAY CONTROL DATA
        # ----------------------------------------------------

        print(
            "TIME:",
            round(
                elapsed,
                1
            ),
            "s",
            "| VAC:",
            round(
                vacuum,
                2
            ),
            "mmHg",
            "| TARGET:",
            TARGET_VACUUM,
            "| ERROR:",
            round(
                error,
                2
            ),
            "| PWM:",
            round(
                pwm,
                1
            ),
            "%",
            "| INT:",
            round(
                controller.integral,
                2
            )
        )


        sleep(
            CONTROL_INTERVAL
        )


# ============================================================
# TEST COMPLETE
# ============================================================

    motor.stop()


    print()
    print("========================================")
    print("CLOSED LOOP TEST COMPLETE")
    print("========================================")

    print("Pump stopped")


# ============================================================
# MANUAL STOP
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
