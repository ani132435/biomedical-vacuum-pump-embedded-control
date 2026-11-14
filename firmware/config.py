"""
Central configuration for the biomedical vacuum pump prototype.

Experimental control settings are kept separate from aspirational
operating-mode targets. These values are not safety-certified limits.
"""

# ============================================================
# HARDWARE CONFIGURATION
# ============================================================

I2C_ID = 0
I2C_SCL_PIN = 1
I2C_SDA_PIN = 0
I2C_FREQUENCY = 400000

MOTOR_PWM_PIN = 2
MOTOR_IN1_PIN = 3
MOTOR_IN2_PIN = 4

MOTOR_PWM_FREQUENCY = 1000


# ============================================================
# EXPERIMENTAL CLOSED-LOOP CONTROL
# ============================================================

TARGET_VACUUM = -2.5       # mmHg gauge

BASE_PWM = 60.0            # percent
MIN_PWM = 40.0             # percent
MAX_PWM = 80.0             # percent

KP = 8.0
KI = 1.0

CONTROL_INTERVAL = 0.1    # seconds
TEST_TIME = 30            # seconds

PRESSURE_FILTER_ALPHA = 0.85
ATMOSPHERE_CALIBRATION_SAMPLES = 30


# ============================================================
# DESIGN TARGETS - NOT VALIDATED OPERATING LIMITS
# ============================================================

TARGET_STIM = -120.0       # mmHg gauge
TARGET_EXPR = -180.0       # mmHg gauge

# Historical design value only. Not a validated safety threshold.
MAX_SAFE_VACUUM = -250.0   # mmHg gauge


# ============================================================
# LEGACY / FUTURE CONFIGURATION
# ============================================================

BUTTON_DEBOUNCE = 50       # milliseconds
ENABLE_LOGGING = True
