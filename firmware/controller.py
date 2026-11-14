class PIController:
    """PI controller with output saturation and conditional integration."""

    def __init__(
        self,
        kp,
        ki,
        integral_min=-100.0,
        integral_max=100.0,
        output_min=-100.0,
        output_max=100.0
    ):
        if integral_min > integral_max:
            raise ValueError("Invalid integral limits")

        if output_min > output_max:
            raise ValueError("Invalid output limits")

        self.kp = kp
        self.ki = ki

        self.integral_min = integral_min
        self.integral_max = integral_max

        self.output_min = output_min
        self.output_max = output_max

        self.integral = 0.0

    def reset(self):
        """Reset the accumulated integral error."""

        self.integral = 0.0

    def update(self, error, dt):
        """Calculate a saturated PI correction."""

        if not dt > 0:
            raise ValueError("dt must be greater than zero")

        proportional = self.kp * error

        candidate_integral = self.integral + error * dt

        candidate_integral = max(
            self.integral_min,
            min(self.integral_max, candidate_integral)
        )

        candidate_output = (
            proportional + self.ki * candidate_integral
        )

        # Reject integration if it pushes the output further
        # into either saturation limit.
        integral_effect = self.ki * error

        pushing_upper_limit = (
            candidate_output > self.output_max
            and integral_effect > 0
        )

        pushing_lower_limit = (
            candidate_output < self.output_min
            and integral_effect < 0
        )

        if not (pushing_upper_limit or pushing_lower_limit):
            self.integral = candidate_integral

        output = proportional + self.ki * self.integral

        return max(
            self.output_min,
            min(self.output_max, output)
        )
