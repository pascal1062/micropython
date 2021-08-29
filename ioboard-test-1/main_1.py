
import machine
import utime

spi = machine.SPI(-1, baudrate=100000, polarity=0, phase=1, sck=machine.Pin(5), mosi=machine.Pin(18), miso=machine.Pin(19))

cs1 = machine.Pin(14, machine.Pin.OUT)
cs1.value(0)
cs2 = machine.Pin(15, machine.Pin.OUT)
cs2.value(0)
cs3 = machine.Pin(27, machine.Pin.OUT)
cs3.value(1)

sleep = 100 

def writeDAC_A(addr, value):
    buf = bytearray(2)
    buf[0] = ((3 << 14) | (addr << 12) | (value << 4)) >> 8
    buf[1] = ((3 << 14) | (addr << 12) | (value << 4)) & 255
    cs1.value(1)
    spi.write(buf)
    cs1.value(0)
    cs1.value(1)
    spi.write(bytes([0x9f, 0xf0]))
    cs1.value(0)

def writeDAC_B(addr, value):
    buf = bytearray(2)
    buf[0] = ((3 << 14) | (addr << 12) | (value << 4)) >> 8
    buf[1] = ((3 << 14) | (addr << 12) | (value << 4)) & 255
    cs2.value(1)
    spi.write(buf)
    cs2.value(0)
    cs2.value(1)
    spi.write(bytes([0x9f, 0xf0]))
    cs2.value(0)

while True:
    for i in range(4):
        writeDAC_A(i,255)
        utime.sleep_ms(sleep)
        writeDAC_A(i,0)
    for i in range(4):
        writeDAC_B(i,255)
        utime.sleep_ms(sleep)
        writeDAC_B(i,0)
    for i in range(4):
        writeDAC_B(3-i,255)
        utime.sleep_ms(sleep)
        writeDAC_B(3-i,0)
    for i in range(4):
        writeDAC_A(3-i,255)
        utime.sleep_ms(sleep)
        writeDAC_A(3-i,0)

#End
