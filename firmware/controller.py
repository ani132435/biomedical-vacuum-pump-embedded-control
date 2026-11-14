class PIController:

    def __init__(
        self,
        kp,
        ki,
        integral_min=-100,
        integral_max=100
    ):

        self.kp = kp
        self.ki = ki

        self.integral = 0

        self.integral_min = integral_min
        self.integral_max = integral_max


    def reset(self):

        self.integral = 0


    def update(
        self,
        error,
        dt
    ):

        # Accumulate error
        self.integral += (
            error
            *
            dt
        )


        # Integral anti-windup
        self.integral = max(
            self.integral_min,
            min(
                self.integral_max,
                self.integral
            )
        )


        # Proportional term
        proportional = (
            self.kp
            *
            error
        )


        # Integral term
        integral_term = (
            self.ki
            *
            self.integral
        )


        # PI output
        output = (
            proportional
            +
            integral_term
        )


        return output
