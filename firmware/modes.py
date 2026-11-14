from config import TARGET_STIM, TARGET_EXPR

class PumpMode:

    STIMULATION = 0

    EXPRESSION = 1

    CUSTOM = 2


def get_target(mode):

    if mode == PumpMode.STIMULATION:

        return TARGET_STIM

    elif mode == PumpMode.EXPRESSION:

        return TARGET_EXPR

    else:

        return TARGET_EXPR
