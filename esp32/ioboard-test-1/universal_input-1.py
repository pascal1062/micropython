import machine

class UniversalInput():

    def __init__(self, instance):
        self._spi = machine.SPI(-1, baudrate=100000, polarity=0, phase=0, sck=machine.Pin(5), mosi=machine.Pin(18), miso=machine.Pin(19))
        self._cs = machine.Pin(27, Pin.OUT)
        self._cs.value(1)
        self._instance = instance
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)

    def read(self):
        channel =  self._instance - 1
        mcp3008_out =  (3 << 6) | (channel << 3)
        self._out_buf[0] = mcp3008_out
        self._out_buf[1] = 0x0
        self._out_buf[2] = 0x0
        self._cs.value(0)scan
        self._spi.write_readinto(out_buf, in_buf)
        self._cs.value(1)
        result = (self._in_buf[0] & 0x01) << 9
        result |= self._in_buf[1] << 1
        result |= self._in_buf[2] >> 7
        return result

    def ad_value(self):
        avg = 0
        sum = 0
        x = 0
        for i in range(5):
            sum = sum + self.read()
            avg = sum / x

        return avg

# End
