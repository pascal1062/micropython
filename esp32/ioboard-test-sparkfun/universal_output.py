'''
    Universal output class
    output can be create as on/off digital or analog dc voltage
    IC chip is TLV5621 connected through SPI serial interface. resoltion is 8 bits 0-255
'''
import machine

class UniversalOutput():

    def __init__(self, instance, type):
        self._spi = machine.SPI(-1, baudrate=100000, polarity=0, phase=1, sck=machine.Pin(5), mosi=machine.Pin(18), miso=machine.Pin(19))
        self._cs1 = machine.Pin(14, machine.Pin.OUT)
        self._cs1.value(0)
        self._cs2 = machine.Pin(15, machine.Pin.OUT)
        self._cs2.value(0)
        self._instance = instance
        self._type = type
        self._dac = None

    def writeDAC_A(self, addr, val):
        buf = bytearray(2)
        buf[0] = ((3 << 14) | (addr << 12) | (val << 4)) >> 8
        buf[1] = ((3 << 14) | (addr << 12) | (val << 4)) & 255
        self._cs1.value(1)
        self._spi.write(buf)
        self._cs1.value(0)
        self._cs1.value(1)
        self._spi.write(bytes([0x9f, 0xf0]))
        self._cs1.value(0)

    def writeDAC_B(self, addr, val):
        buf = bytearray(2)
        buf[0] = ((3 << 14) | (addr << 12) | (val << 4)) >> 8
        buf[1] = ((3 << 14) | (addr << 12) | (val << 4)) & 255
        self._cs2.value(1)
        self._spi.write(buf)
        self._cs2.value(0)
        self._cs2.value(1)
        self._spi.write(bytes([0x9f, 0xf0]))
        self._cs2.value(0)

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
            self.writeDAC_A(1, dac_value)
        elif inst == 2:
            self.writeDAC_A(0, dac_value)
        elif inst == 3:
            self.writeDAC_A(2, dac_value)
        elif inst == 4:
            self.writeDAC_A(3, dac_value)
        elif inst == 5:
            self.writeDAC_B(1, dac_value)
        elif inst == 6:
            self.writeDAC_B(0, dac_value)
        elif inst == 7:
            self.writeDAC_B(2, dac_value)
        elif inst == 8:
            self.writeDAC_B(3, dac_value)

    #Set Property
    value = property(get_value, set_value)

# End
