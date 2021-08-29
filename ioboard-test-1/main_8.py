#machine import
import time
import ujson
from universal_input import UniversalInput
from universal_output import UniversalOutput
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from on_off_bdc import OnOffBDC

#mqtt import
from ubinascii import hexlify
from machine import unique_id
from umqtt.simple import MQTTClient

#automation import
import irrig_pump_program
import light_program

#scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()
on_off = OnOffBDC()

#inputs
AI1 = UniversalInput(1, "analog", aic10K)
AI4 = UniversalInput(4, "analog", percentRev)
BI8 = UniversalInput(8, "binary", on_off)

#outputs
BO1 = UniversalOutput(1, "binary")
BO2 = UniversalOutput(2, "binary")
BO3 = UniversalOutput(3, "binary")
BO4 = UniversalOutput(4, "binary")
BO5 = UniversalOutput(5, "binary")
BO6 = UniversalOutput(6, "binary")
BO7 = UniversalOutput(7, "binary")
BO8 = UniversalOutput(8, "binary")

#variables
irrig_start_time = time.mktime(time.localtime())
irrig_stop_time = irrig_start_time
stop_board = False
counter = 0

#analog inputs values for filters
last_value_AI1 = 1024 / 2
last_value_AI4 = 1024 / 2

#binary inputs compare (if needed)
last_state_BI8 = "Off"

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()

#stops board (...for webrepl...and ftp server...)
def _stop():
    global stop_board
    stop_board = True

#reset board
def _reset():
    import machine
    machine.reset()

#mqtt client
def sub_cb(topic, msg):
    if topic == b'/output/BO2' and 0 <= int(msg) <= 255: BO2.value = int(msg)
    if topic == b'/system/exit' and msg == b'Exit': _stop()

#mqtt connect and subscribe to Broker
def connect_and_subscribe():
    _client = MQTTClient(hexlify(unique_id()), '192.168.0.149')
    _client.set_callback(sub_cb)
    _client.connect()
    _client.subscribe(b'/output/BO2')
    _client.subscribe(b'/system/exit')
    return _client

#mqtt start
try:
    client = connect_and_subscribe()
except:
    pass


#main loop execution
while True:
    if stop_board: break
    #analog input filters
    temperature = AI1.value + (10.0 / 100.0) * (AI1.value - last_value_AI1)
    last_value_AI1 = temperature
    photocell = AI4.value + (10.0 / 100.0) * (AI4.value - last_value_AI4)
    last_value_AI4 = photocell

    #automation program for control of irrigation pump
    result = irrig_pump_program.execute(BI8.value, BO1.value, last_state_BI8, irrig_start_time, irrig_stop_time, 1)
    BO1.value = result[0]
    last_state_BI8 = result[1]
    irrig_start_time = result[2]
    irrig_stop_time = result[3]

    #automation program for light control on based on schedule
    result = light_program.execute(time.localtime(), 1800, 1830)
    BO5.value = result
    result = light_program.execute(time.localtime(), 0600, 2200)
    BO3.value = result

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO8.value = 255 if BO8.value == 0 else 0
        timer_1 = time.ticks_ms()

    #mqtt check for messages
    try:
        client.check_msg()
    except:
        pass

    #mqtt reconnect after 5 minutes of each tries OR reset board after 60 minutes
    if counter == 5 or counter == 10 or counter == 15 or counter == 20 or counter == 25 or counter == 30:
        try:
            client = connect_and_subscribe()
        except:
            pass
    if counter == 60: _reset()

    #mqtt publish (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 60000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        irrig_start = time.localtime(irrig_start_time)
        irrig_stop = time.localtime(irrig_stop_time)
        irrig_obj = {"value": BO1.value, "start": irrig_start, "stop": irrig_stop}
        irrig_json = ujson.dumps(irrig_obj)

        try:
            client.publish('ioboard/rtc_time', date_str+" "+time_str)
            client.publish('ioboard/irrigation', irrig_json)
            counter = 0
        except:
            counter += 1
            pass

        scan_time = time.ticks_ms()

#Fin
