import machine

last_value = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

class UniversalInput():

    def __init__(self, instance, type, scale):
        self._spi = machine.SPI(-1, baudrate=100000, polarity=0, phase=0, sck=machine.Pin(5), mosi=machine.Pin(18), miso=machine.Pin(19))
        self._cs = machine.Pin(27, machine.Pin.OUT)
        self._cs.value(1)
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)
        self._instance = instance
        self._type = type
        self._scale = scale

    def read(self):
        channel =  self._instance - 1
        mcp3008_out =  (3 << 6) | (channel << 3)
        self._out_buf[0] = mcp3008_out
        self._out_buf[1] = 0x0
        self._out_buf[2] = 0x0
        self._cs.value(0)
        self._spi.write_readinto(self._out_buf, self._in_buf)
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
            x += 1
            avg = sum / x

        return avg

    def volt(self):
        vcc = 3.3
        v = round(self.ad_value() * (vcc / 1023.0),3)
        return v

    def aic(self):
        global last_value
        channel =  self._instance - 1
        sr = self._scale
        l = len(sr.SCALE_RANGE)
        v = self.volt()
        result = 0.0
        diff_calc = 0.0
        diff_volt = 0.0
        present_value = 0.0

        reverse = True if sr.SCALE_RANGE[0][1] > sr.SCALE_RANGE[29][1] else False

        if reverse:
            if v <= sr.SCALE_RANGE[0][0]:
                result = sr.SCALE_RANGE[0][1]
            elif v >= sr.SCALE_RANGE[29][0]:
                result = sr.SCALE_RANGE[29][1]
            else:
                for i in range(0,l-1):
                    if v >= sr.SCALE_RANGE[i][0] and v <= sr.SCALE_RANGE[i+1][0]:
                        diff_volt = sr.SCALE_RANGE[i+1][0] - sr.SCALE_RANGE[i][0]
                        diff_calc = sr.SCALE_RANGE[i][1] - sr.SCALE_RANGE[i+1][1]
                        result = sr.SCALE_RANGE[i][1] - ((v - sr.SCALE_RANGE[i][0]) / ( diff_volt / diff_calc))
        else:
            if v <= sr.SCALE_RANGE[0][0]:
                result = sr.SCALE_RANGE[0][1]
            elif v >= sr.SCALE_RANGE[29][0]:
                result = sr.SCALE_RANGE[29][1]
            else:
                for i in range(0,l-1):
                    if v >= sr.SCALE_RANGE[i][0] and v <= sr.SCALE_RANGE[i+1][0]:
                        diff_volt = sr.SCALE_RANGE[i+1][0] - sr.SCALE_RANGE[i][0]
                        diff_calc = sr.SCALE_RANGE[i+1][1] - sr.SCALE_RANGE[i][1]
                        result = sr.SCALE_RANGE[i+1][1] - (( sr.SCALE_RANGE[i+1][0] - v) / ( diff_volt / diff_calc))

        ''' Present Value = Last Value + (( 100 - Filter ) / 100 * ( Input Value - Last Value )) '''
        #present_value = last_value + (10.0 / 100.0 * (result - last_value))
        #last_value = result
        present_value = last_value[channel] + (10.0 / 100.0 * (result - last_value[channel]))
        last_value[channel] = result
        return present_value

    def bdc(self):
        sr = self._scale
        v = self.volt()
        result = None
        if v <= 1:
            result = sr.SCALE_RANGE[0][1]
        elif v >= 2:
            result = sr.SCALE_RANGE[1][1]
        return result

    @property
    def value(self):
        if  self._type == "analog":
            val = self.aic()
        elif self._type == "binary":
            val = self.bdc()

        return val

# End
