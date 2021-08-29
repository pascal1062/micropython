
# machine import
import time
from machine import Pin

from ai import AnalogInput
from bi import BinaryInput
from bo import BinaryOutput
from av import AnalogValue
from bv import BinaryValue
from timer import Timer
from data_exchange import DataExchange
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from automation import Automation as func
import light_program

# network data excchange
xfer = DataExchange()
xfer.attach('192.168.0.51')
read = None
SERVER_ADDR = "192.168.0.149"

# scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()

# inputs
AI1 = AnalogInput(1, "t_ext", 85.0, 0.0, aic10K)
AI2 = AnalogInput(2, "t_piscine", 85.0, 0.0, aic10K)
AI3 = AnalogInput(3, "t_panneau", 85.0, 0.0, aic10K)
AI4 = AnalogInput(4, "photocell", 85.0, 0.0, percentRev)
BI8 = BinaryInput(8, "bouton", False)
stop_button = Pin(0, Pin.IN, Pin.PULL_UP)

# outputs
BO1 = BinaryOutput(1, "chauff_panneau")
BO2 = BinaryOutput(2, "sortie2")
BO3 = BinaryOutput(3, "sortie3")
BO4 = BinaryOutput(4, "sortie4")
BO5 = BinaryOutput(5, "sortie5")
BO6 = BinaryOutput(6, "sortie6")
BO7 = BinaryOutput(7, "sortie7")
BO8 = BinaryOutput(8, "pompe_irrig")
scan_led = Pin(13, Pin.OUT)
# default value
BO1.value = False
BO2.value = False
BO3.value = False
BO4.value = False
BO5.value = False
BO6.value = False
BO7.value = False
BO8.value = False

#variables
stop_board = BinaryValue(1, "stop-board")

#first scan
AI1.value; AI2.value; AI3.value; AI4.value; BI8.value

#miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()
timer_3 = time.time()

#function return date-time
def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str

def ioData():
    board = {"AI1": temperature, "AI5": photocell, "BI2": BI2.value, "BO1": BO1.value, "BO2": BO2.value, "BO3": BO3.value,
             "BO4": BO4.value, "BO5": BO5.value, "BO6": BO6.value, "BO7": BO7.value, "BO8": BO8.value, "board": "ioboard_cab", "route": "nred"
    }
    
#function stop board
def _stop():
    xfer.send_data({"route": "nred", "board": "ioboard_cab", "state": "stop command received..."}, SERVER_ADDR)
    import gc
    gc.collect()
    import sys
    sys.exit()
    
#function set time clock
def _settime():
    import network_rtc
    network_rtc.set_time()
    xfer.send_data({"route": "nred", "board": "ioboard_cab", "time": actualTime(time.localtime())}, SERVER_ADDR)
    

#boot wait 1 sec
xfer.send_data({"route": "nred", "board": "ioboard_cab", "state": "booting wait 1 sec..."}, SERVER_ADDR)
time.sleep(1)
xfer.send_data({"route": "nred", "board": "ioboard_cab", "time": actualTime(time.localtime())}, SERVER_ADDR)


#main loop execution
while True:
    
    #stop board from network or on board button
    if stop_board.value: _stop()
    if stop_button.value() == 0: _stop()
    
    # Read data transfer
    read = xfer.recv_data()
    if read is not None:
        if read[0] == "/ioboard_cab/system/exit" and read[1] == "True": stop_board.value = True
        if read[0] == "/ioboard_cab/valve": _irrig(read[1])
        if read[0] == "/ioboard_cab/settime" and read[1] == "True": _settime()
        if read[0] == "/ioboard_cab/gettime" and read[1] == "True": xfer.send_data({"route": "nred", "board": "ioboard_cab", "time": actualTime(time.localtime())}, SERVER_ADDR)

    #scan inputs not used in automation process...    
    temp_ext = AI1.value; temp_pisc = AI2.value; temp_pan = AI3.value; photo = AI4.value; BI8.value
    
    #chauffage panneau
    BO1.value = func.aswitch(BO1.value, temp_pan, 5.0, 10.0)
    
    #Test avec bouton et sortie 8
    if BI8.rising(): BO8.value = not BO8.value
        
    #sync time every hour
    if (time.time() - timer_2) >= 3600:
        _settime()
        timer_2 = time.time()

    #led flasher light_program 200 msec
    if time.ticks_diff(time.ticks_ms(), timer_1) > 200:
        scan_led.value(1) if scan_led.value() == 0 else scan_led.value(0)
        timer_1 = time.ticks_ms()
        
    #send I/O data every 5 minutes
    if (time.time() - timer_3) >= 300:
        _settime()
        timer_3 = time.time()        

#Fin