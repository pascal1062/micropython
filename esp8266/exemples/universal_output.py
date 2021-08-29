'''
    Universal output class with IOBoard
    output can be create as on/off digital or analog dc voltage
    IOBoard connected through I2C serial interface. resoltion is 8 bits 0-255
'''
from machine import Pin, I2C

class UniversalOutput():

    def __init__(self, instance, type):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=20000)
        self._outaddr = [85, 86, 87, 88, 89, 90, 91,92]
        self._instance = instance
        self._type = type
        self._dac = None

    def writeToOuputs(self, idx, val):
        buf = bytearray(2)
        buf[0] = self._outaddr[idx]
        buf[1] = val
        self._i2c.writeto(0x13, buf)

    def get_value(self):
        return self._dac

    def set_value(self, val):
        self._dac = val
        inst = self._instance

        if isinstance(self._dac, bool):
            if self._dac == True:
                dac_value = 255
            else:
                dac_value = 0
        elif isinstance(self._dac, int):
            dac_value = self._dac
        else:
            dac_value = 0

        if inst == 1:
            self.writeToOuputs(0, dac_value)
        elif inst == 2:
            self.writeToOuputs(1, dac_value)
        elif inst == 3:
            self.writeToOuputs(2, dac_value)
        elif inst == 4:
            self.writeToOuputs(3, dac_value)
        elif inst == 5:
            self.writeToOuputs(4, dac_value)
        elif inst == 6:
            self.writeToOuputs(5, dac_value)
        elif inst == 7:
            self.writeToOuputs(6, dac_value)
        elif inst == 8:
            self.writeToOuputs(7, dac_value)

    #Set Property
    value = property(get_value, set_value)

# End
