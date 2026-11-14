from machine import I2C
from time import sleep_ms
import struct

class BMP280:

    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr

        # Check sensor
        chip = self.i2c.readfrom_mem(self.addr, 0xD0, 1)[0]
        if chip != 0x58:
            raise Exception("BMP280 not detected")

        # Normal mode
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')
        self.i2c.writeto_mem(self.addr, 0xF5, b'\x00')
        sleep_ms(100)

        self.read_calibration()

    def read_u16(self, reg):
        return struct.unpack("<H", self.i2c.readfrom_mem(self.addr, reg, 2))[0]

    def read_s16(self, reg):
        return struct.unpack("<h", self.i2c.readfrom_mem(self.addr, reg, 2))[0]

    def read_calibration(self):

        self.T1 = self.read_u16(0x88)
        self.T2 = self.read_s16(0x8A)
        self.T3 = self.read_s16(0x8C)

        self.P1 = self.read_u16(0x8E)
        self.P2 = self.read_s16(0x90)
        self.P3 = self.read_s16(0x92)
        self.P4 = self.read_s16(0x94)
        self.P5 = self.read_s16(0x96)
        self.P6 = self.read_s16(0x98)
        self.P7 = self.read_s16(0x9A)
        self.P8 = self.read_s16(0x9C)
        self.P9 = self.read_s16(0x9E)

    def read_raw(self):

        data = self.i2c.readfrom_mem(self.addr, 0xF7, 6)

        raw_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        raw_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        return raw_p, raw_t

    def read(self):

        raw_p, raw_t = self.read_raw()

        var1 = (raw_t / 16384.0 - self.T1 / 1024.0) * self.T2
        var2 = ((raw_t / 131072.0 - self.T1 / 8192.0) ** 2) * self.T3

        t_fine = var1 + var2

        temperature = t_fine / 5120.0

        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.P6 / 32768.0
        var2 += var1 * self.P5 * 2.0
        var2 = var2 / 4.0 + self.P4 * 65536.0

        var1 = (self.P3 * var1 * var1 / 524288.0 +
                self.P2 * var1) / 524288.0

        var1 = (1.0 + var1 / 32768.0) * self.P1

        if var1 == 0:
            return None

        pressure = 1048576.0 - raw_p
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1

        var1 = self.P9 * pressure * pressure / 2147483648.0
        var2 = pressure * self.P8 / 32768.0

        pressure += (var1 + var2 + self.P7) / 16.0

        pressure_pa = pressure
        pressure_hpa = pressure / 100.0
        pressure_mmhg = pressure_hpa * 0.750062

        return {
            "temperature": temperature,
            "pressure_pa": pressure_pa,
            "pressure_hpa": pressure_hpa,
            "pressure_mmhg": pressure_mmhg
        }
