'''
    replace data network data echanges with UDP sockets instead of mqtt
'''

# machine import
import time
from ai import AnalogInput
from bi import BinaryInput
from bo import BinaryOutput
from av import AnalogValue
from bv import BinaryValue
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from timer import Timer
import light_program
from data_exchange import DataExchange

# network data excchange
xfer = DataExchange()
xfer.attach('192.168.0.50')
read = None
SERVER_ADDR = "192.168.0.149"

# scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()

# inputs
AI1 = AnalogInput(1, "temp", 80, aic10K)
BI2 = BinaryInput(2, "etat-relais")
AI5 = AnalogInput(5, "photocell", 80, percentRev)
BI8 = BinaryInput(8, "bouton")

# outputs
BO1 = BinaryOutput(1, "pompe1")
BO2 = BinaryOutput(2, "BO2")
BO3 = BinaryOutput(3, "pompe2")
BO4 = BinaryOutput(4, "BO4")
BO5 = BinaryOutput(5, "light")
BO6 = BinaryOutput(6, "BO6")
BO7 = BinaryOutput(7, "flasher")
BO8 = BinaryOutput(8, "lampe")
# not used
BO1.value = False
BO2.value = False
BO3.value = False
BO4.value = False
BO5.value = False
BO6.value = False
BO7.value = False
BO8.value = False

# variables
stop_board = BinaryValue(1, "stop-board")

# variables for irrigation throuh MQTT
irrig = BinaryValue(2, "irrigation_start")
irrig_time = AnalogValue(2, "irrigation_time")

# first scan
AI1.value; AI5.value

# scan rate time (if needed)
scan_time = time.ticks_ms()

# miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()
t1 = Timer()
t3 = Timer()

# wait time for ctrl-C at boot
xfer.send_data({"route": "nred", "board": "esp8266", "state": "booting wait 10 sec..."}, SERVER_ADDR)
time.sleep(10)

#stop board
def _stop():
    xfer.send_data({"route": "nred", "board": "esp8266", "state": "stop command received..."}, SERVER_ADDR)
    import gc
    gc.collect()
    import sys
    sys.exit()

# reset board
def _reset():
    import machine
    machine.reset()

#irrigation start for desired time
def _irrig(t):
    irrig_time.value = int(t) * 60 if t.isdigit() else irrig_time.value
    if irrig_time.value > 0: BO3.value = True; t3.stop(); t3.start()
    else: BO3.value = False; t3.stop(); xfer.send_data({"route": "mqtt", "board": "esp8266", "countdown": 0}, SERVER_ADDR)
    
#set time clock
def _settime():
    import network_rtc
    network_rtc.set_time()    

xfer.send_data({"route": "mqtt", "board": "esp8266", "countdown": 0}, SERVER_ADDR)

# main loop execution
while True:
    # Read data transfer
    read = xfer.recv_data()
    if read is not None:
        if read[0] == "/esp8266/system/exit" and read[1] == "True": stop_board.value = True
        if read[0] == '/esp8266/valve': _irrig(read[1])
        if read[0] == '/esp8266/settime': _settime()

    if stop_board.value: _stop()

    # Inputs miscellanous
    temperature = AI1.value; photocell = AI5.value
    BI2.value; BI8.value

    # automation program for control of irrigation pump BO1
    if t1.running() and (t1.elapsed() >= 60): t1.stop(); BO1.value = False
    if BI8.rising(): BO1.value = True; t1.stop(); t1.start()

    # automation program for irrigation pump BO3 through UDP xfer
    if t3.running() and t3.changed(60): xfer.send_data({"route": "mqtt","board": "esp8266", "countdown": (irrig_time.value - t3.elapsed())/60}, SERVER_ADDR)
    if t3.running() and (irrig_time.value - t3.elapsed()) <= 0: t3.stop(); BO3.value = False
    if BI2.changed(): xfer.send_data({"route": "mqtt", "board": "esp8266", "valve": str(BI2.value)}, SERVER_ADDR)

    # automation program for light control on based on schedule
    result = light_program.execute(time.localtime(), 0600, 1830)
    BO5.value = result
    result = light_program.execute(time.localtime(), 2000, 2200)
    BO8.value = result

    # led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO7.value = not BO7.value
        timer_1 = time.ticks_ms()

    # sync time every hour
    if (time.time() - timer_2) >= 3600:
        _settime()
        timer_2 = time.time()

    # mqtt publish (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 60000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        board = {"AI1": temperature, "AI5": photocell, "BI2": BI2.value, "BO1": BO1.value, "BO2": BO2.value, "BO3": BO3.value,
                 "BO4": BO4.value, "BO5": BO5.value, "BO6": BO6.value, "BO7": BO7.value, "BO8": BO8.value, "board": "esp8266", 
                 "time": time_str, "date": date_str, "route": "nred"}

        xfer.send_data(board, SERVER_ADDR)
        if not t3.running(): 
            xfer.send_data({"route": "mqtt", "board": "esp8266", "countdown": 0}, SERVER_ADDR)
            xfer.send_data({"route": "mqtt", "board": "esp8266", "valve": str(BI2.value)}, SERVER_ADDR)

        scan_time = time.ticks_ms()

# Fin