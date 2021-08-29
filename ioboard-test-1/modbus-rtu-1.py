
from universal_output import UniversalOutput
from uModBus.serial import Serial
#import time
#from machine import UART
#uart = UART(2, 9600)
#uart.init(9600, bits=8, parity=None, stop=1, tx=17, rx=16, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0)
#uart.init(9600, bits=8, parity=None, stop=1)

#T1_5 = 1750 #16500000//9600
#T3_5 = 4010 #(3500000 * (8 + 1 + 2))//9600

modbus_rtu = Serial(2,38400)
#frame = [None] * 128

modbus_rtu._uart_read_frame()

while True:
    mrequest = modbus_rtu.get_request([1])
    if mrequest is not None:
        print(mrequest)
