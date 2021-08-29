#machine import
import time 
from machine import Pin
from machine import PWM

from data_exchange import DataExchange 
from av import AnalogValue
from bv import BinaryValue
from automation import Automation

#network data excchange
xfer = DataExchange()
xfer.attach('192.168.0.55', 47906)
read = None
SERVER_ADDR = "192.168.0.149"

#variables
stop_board = BinaryValue(1, "stop-board")
counter = AnalogValue(1, "compteur")
dim = AnalogValue(2, "dimming")

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()

led = Pin(5, Pin.OUT, value=1)
led22 = Pin(22, Pin.OUT, value=0)
pwm22 = PWM(led22); pwm22.freq(1000); pwm22.duty(0)

#reset board
def _reset():
    import machine
    machine.reset()

#wait time for ctrl-C at boot
xfer.send_data({"route": "nred", "board": "lonin32", "state": "booting wait 10 sec..."}, SERVER_ADDR, 47906)
time.sleep(10)   

#main loop execution
while True:
    #Read data transfer
    read = xfer.recv_data()
    if read != None:
        if read[0] == "/lonin32/system/exit" and read[1] == "True": stop_board.value = True  
        if read[0] == '/lonin32/led22': dim.value = int(read[1]) if read[1].isdigit() else dim.value
       
    if stop_board.value: break

    #control led GPIO 22, pwm dimming
    pwm22.duty(int(Automation.scale(dim.value,0,100,0,512)))  

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
    if time.ticks_diff(time.ticks_ms(), scan_time) > 60000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        led22_state = str(round(Automation.scale(pwm22.duty(),0,512,0,100),1))+" %"
        board = {"route": "nred", "board":"lonin32", "date":date_str, "time":time_str, "led22":led22_state}
        

        xfer.send_data(board, SERVER_ADDR, 47906)
        #print(board)

        scan_time = time.ticks_ms()

#Fin 