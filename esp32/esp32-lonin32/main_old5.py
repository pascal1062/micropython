#machine import
import time
import ujson
from machine import Pin

from data_exchange import DataExchange 
from av import AnalogValue
from bv import BinaryValue

#network data excchange
xfer = DataExchange("192.168.0.55", 47904)
xfer.attach()
read = None
SERVER_ADDR = "192.168.0.149"

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
    read = xfer.recv_data()

    #analyse received data
    if read != None:
        #if read.keys() == "lonin32-stop" and read.values() == 'True': stop_board.value = True 
        #if "lonin32-stop" in read.keys(): stop_board.value = True if read["lonin32-stop"] == "True" else False
        if "stop_board" in read: stop_board.value = True if read["stop_board"] == "True" else False
        #if read.keys() == "lonin32-msg": print(read.values())
        #if "lonin32-msg" in read.keys(): print(read["lonin32-msg"])
        if "message" in read: print(read["message"])
       
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


    #msend data to node-red server through UDP (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 30000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])

        xfer.send_data("lonin32 " + date_str+" "+time_str, SERVER_ADDR, 47905)
        print("lonin32 " + date_str+" "+time_str)

        scan_time = time.ticks_ms()

#Fin 