from machine import Pin, I2C
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=50000)

#i2c.scan()

output_addr = [85, 86, 87, 88, 89, 90, 91,92]

def writeToOuputs(idx, val):
    global output_addr
    buf = bytearray(2)
    buf[0] = output_addr[idx]
    buf[1] = val
    i2c.writeto(0x13, buf)

#send outputs "ON" with 200msec interval and then send to "OFF" with 200msec interval
while True:
    for i in range(0,8,1):
        writeToOuputs(i, 255)
        time.sleep(0.2)
    for i in range(7,-1,-1):
        writeToOuputs(i, 0)
        time.sleep(0.2)

inputs = bytearray(20)
i2c.readfrom_into(0x13, inputs)
#results
#bytearray(b'\x00\x10\x03\xff\x03\xff\x03\xff\x03\xff\x03\xff\x03\xfe\x03\xfe\x03\xfe\x12m')
#fisrt 2 bytes are announciation only...no data
#last 2 bytes xfe\x12m are CRC checking
#get input #1 --> inputs[2]<<8 | inputs[3]

#def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3536.14):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

R = 10000 / (1024/AD_value - 1)

while True:
    i2c.readfrom_into(0x13, inputs)
    AI1 = inputs[2]<<8 | inputs[3]
    R = 10000 / (1024/AI1 - 1)                                                                                                                    
    steinhart_temperature_C(R)
    time.sleep(1)
