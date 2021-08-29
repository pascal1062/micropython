from machine import Pin, I2C
import time

class AnalogInput():

    def __init__(self, instance, name, filter, scale):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=20000)
        self._buf = bytearray(20)
        self._instance = instance
        self._name = name
        self._scale = scale
        self._filter = filter
        self._scan = 0
        self._newvalue = 0.0
        self._lastvalue = 0.0

    def calculate_crc(b, l):
        crc = 0xFFFF
        crcH = 0
        crcL = 0

        for i in range(0,l,1):
            crc ^= b[i]
            for j in range(8,0,-1):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1

        #bytes are wrong way round so doing a swap here..
        crcH = (crc & 0x00FF) << 8
        crcL = (crc & 0xFF00) >> 8
        crcH |= crcL
        crc = crcH
        return crc

    def read(self):
        result = 0
        inputCRC = 0
        calcCRC = 0
        channel =  self._instance - 1
        #Result Bytes should be this: [0,16,H1,L1,H2,L2,H3,L3,H4,L4,H5,L5,H6,L6,H7,L7,H8,L8,crcHIGH,crcLOW]
        self._i2c.readfrom_into(0x13, self._buf)

        if (self._buf[2] == 16) and (len(self._buf) == 20):
            inputCRC = self._buf[18] << 8 | self._buf[19]
            calcCRC = self.calculate_crc(self._buf[2:18], 16)

        if ((calcCRC - inputCRC) == 0):
            for i in range(8):
                if i == channel:
                    result = self._buf[i+(i+2)]<<8 | self._buf[i+(i+3)]
                    break

        return result

    def ad_value(self):
        rd = self.read()
        return rd

    def volt(self):
        vcc = 5
        v = round(self.ad_value() * (vcc / 1023.0),3)
        return v

    def aic(self):
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

        return result

    @property
    def value(self):
        if time.ticks_diff(time.ticks_ms(), self._scan) > 53:
            self._scan = time.ticks_ms()
            self._newvalue = self.aic()
            filtered = self._lastvalue + (( 100 - self._filter) / 100 * (self._newvalue - self._lastvalue))
            self._lastvalue = self._newvalue
            return filtered

    @property
    def name(self):
        return self._name

# End
