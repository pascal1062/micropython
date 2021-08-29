#machine import
import time
import ujson
import socket
from machine import Pin

from av import AnalogValue
from bv import BinaryValue

#network variables
LOCAL_ADDR = "192.168.0.55"
SERVER_ADDR = "192.168.0.149"
PORT = 47902
data = None
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((LOCAL_ADDR, PORT))
s.settimeout(0.001)

#variables
stop_board = BinaryValue(1, "stop-board")
counter = AnalogValue(1, "compteur")

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()

led = Pin(5, Pin.OUT)

#reset board
def _reset():
    import machine
    machine.reset()

#wait time for ctrl-C at boot
time.sleep(10)    

#main loop execution
while True:
    try:
        data = None
        data = s.recv(128)
    except:
        pass

    #analyse received data
    if data == b'/lonin32/system/exit': stop_board.value = True 
    if data == b'/lonin32/message/Hello': print("Hello")  
       
    if stop_board.value: break 

    #sync time every hour
    if (time.time() - timer_2) >= 3600:
        import network_rtc
        network_rtc.set_time()
        timer_2 = time.time()

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 100:
        led.value(0) if led.value() == 1 else led.value(1)
        timer_1 = time.ticks_ms()


    #mqtt publish (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 30000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])

        s.sendto("lonin32 date-time " + date_str+" "+time_str, (SERVER_ADDR, 47903))  
        print("lonin32 " + date_str+" "+time_str)

        scan_time = time.ticks_ms()

#Fin 