import time
from machine import Pin, I2C

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=50000)

button = Pin(12, Pin.IN, Pin.PULL_UP)

def writeToOuputs(idx, val):
    i2c_addr = 0x13
    output_addr = [85, 86, 87, 88, 89, 90, 91,92]
    buf = bytearray(2)
    buf[0] = output_addr[idx]
    buf[1] = val
    i2c.writeto(i2c_addr, buf)

#send outputs "ON" with 200msec interval and then send to "OFF" with 200msec interval
while True:
    for i in range(0,8,1):
        writeToOuputs(i, 255)
        time.sleep(0.2)
    for i in range(7,-1,-1):
        writeToOuputs(i, 0)
        time.sleep(0.2)

    if button.value() == 1: break

#End
