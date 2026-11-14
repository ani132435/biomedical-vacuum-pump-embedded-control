# PressureSensor.py

class PressureSensor:

    def __init__(self, bmp):
        self.bmp = bmp
        self.atm_pressure = bmp.pressure

    def pressure(self):
        return self.bmp.pressure

    def vacuum(self):
        return self.bmp.pressure - self.atm_pressure
