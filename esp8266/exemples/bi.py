from machine import Pin, I2C
import time

class BinaryInput():

    def __init__(self, instance, name):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=20000)
        self._buf = bytearray(20)
        self._instance = instance
        self._name = name
        self._scan = 0
        self._count = 0
        self._sum = 0.0
        self._avg = 0.0
        self._newvalue = False
        self._lastvalue = False

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

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        if self._newvalue != self._lastvalue:
            val = self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def falling(self):
        if (self._newvalue != self._lastvalue):
            val = not self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    @property
    def value(self):
        if time.ticks_diff(time.ticks_ms(), self._scan) > 7:
            self._scan = time.ticks_ms()
            self._count += 1
            self._sum += self.volt()
            self._avg = self._sum  / self._count

        if self._count >= 3:
            if self._avg <= 1.5:
                self._newvalue = True
            elif self._avg >= 3.5:
                self._newvalue = False

            self._count = 0; self._sum = 0.0

        return self._newvalue

    @property
    def name(self):
        return self._name

#End
