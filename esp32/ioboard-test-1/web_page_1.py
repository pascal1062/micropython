#import machine
#pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
import time
from universal_input import UniversalInput
from thermistor10KDegC import Thermistor10KCelsius
from universal_output import UniversalOutput

aic10K = Thermistor10KCelsius()

AI1 = UniversalInput(1, "analog", aic10K)
BO2 = UniversalOutput(2, "binary")
BO2.value = 0

html = '<!DOCTYPE html><html><head> <title>ESP8266 Pins</title> </head><body> <h1>ESP8266 Pins</h1><table border="1"> <tr><th>Pin</th><th>Value</th></tr></table></body></html>'

import socket
addr = socket.getaddrinfo('192.168.0.124', 8080)[0][-1]

s = socket.socket()
#s.bind(addr)
s.bind(('192.168.0.124', 8080))
s.listen(1)

print('listening on', addr)

timer_1 = time.ticks_ms()

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    #rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str("AI1"), AI1.value)]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO2.value = 255 if BO2.value == 0 else 0
        timer_1 = time.ticks_ms()
