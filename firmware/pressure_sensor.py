from bmp280 import BMP280

class PressureSensor:

    def __init__(self, i2c):

        self.bmp = BMP280(i2c)

    def read(self):

        data = self.bmp.read()

        return data["pressure_mmhg"]
