'''
    Universal output class with IOBoard
    output can be create as on/off digital or analog dc voltage
    IOBoard connected through I2C serial interface. resoltion is 8 bits 0-255
'''
from machine import Pin, I2C

class BinaryOutput():

    def __init__(self, instance, name):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=20000)
        self._outaddr = [85, 86, 87, 88, 89, 90, 91,92]
        self._instance = instance
        self._name = name
        self._newvalue = None
        self._lastvalue = None

    def _writeToOuputs(self, idx, val):
        buf = bytearray(2)
        buf[0] = self._outaddr[idx]
        buf[1] = val
        self._i2c.writeto(0x13, buf)

    def get_name(self):
        return self._name

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, bool):
            self._newvalue = val
            dac_value = 255 if self._newvalue == True else False
        else:
            return

        if self._instance == 1:
            self._writeToOuputs(0, dac_value)
        elif self._instance == 2:
            self._writeToOuputs(1, dac_value)
        elif self._instance == 3:
            self._writeToOuputs(2, dac_value)
        elif self._instance == 4:
            self._writeToOuputs(3, dac_value)
        elif self._instance == 5:
            self._writeToOuputs(4, dac_value)
        elif self._instance == 6:
            self._writeToOuputs(5, dac_value)
        elif self._instance == 7:
            self._writeToOuputs(6, dac_value)
        elif self._instance == 8:
            self._writeToOuputs(7, dac_value)

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def falling(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue == False):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)

#End
