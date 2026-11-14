from time import sleep_ms
from bmp280_sensor import BMP280


class PressureSensor:
    """BMP280 absolute-pressure sensor with filtering and gauge calibration."""

    def __init__(self, i2c, addr=0x76, alpha=0.85):
        if not 0.0 <= alpha < 1.0:
            raise ValueError("alpha must be >= 0 and < 1")

        self.bmp = BMP280(i2c, addr)
        self.alpha = alpha

        self.filtered_pressure = None
        self.atm_pressure = None

    @staticmethod
    def _get_pressure(data):
        """Extract and validate absolute pressure in mmHg."""

        if data is None:
            raise ValueError("BMP280 returned no data")

        pressure = data.get("pressure_mmhg")

        if pressure is None or not (pressure > 0):
            raise ValueError("Invalid BMP280 pressure reading")

        return pressure

    def read(self):
        """Return filtered absolute pressure in mmHg."""

        data = self.bmp.read()
        pressure = self._get_pressure(data)

        if self.filtered_pressure is None:
            self.filtered_pressure = pressure
        else:
            self.filtered_pressure = (
                self.alpha * self.filtered_pressure
                + (1.0 - self.alpha) * pressure
            )

        return self.filtered_pressure

    def calibrate_atmosphere(self, samples=30, interval_ms=50):
        """Establish atmospheric reference using absolute-pressure samples."""

        if not isinstance(samples, int) or samples < 1:
            raise ValueError("samples must be a positive integer")

        if not isinstance(interval_ms, int) or interval_ms < 0:
            raise ValueError("interval_ms must be a non-negative integer")

        total = 0.0

        for index in range(samples):
            data = self.bmp.read()
            total += self._get_pressure(data)

            if index < samples - 1 and interval_ms > 0:
                sleep_ms(interval_ms)

        self.atm_pressure = total / samples
        self.filtered_pressure = self.atm_pressure

        return self.atm_pressure

    def vacuum(self):
        """Return gauge vacuum in mmHg; negative means below atmosphere."""

        if self.atm_pressure is None:
            raise RuntimeError("Atmospheric calibration required")

        return self.read() - self.atm_pressure
