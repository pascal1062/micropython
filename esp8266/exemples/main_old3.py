#machine import
import time
import ujson
from universal_input import UniversalInput
from bo import BinaryOutput
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from on_off_bdc import OnOffBDC
from timer import Timer

#mqtt import
from ubinascii import hexlify
from machine import unique_id
from umqtt.simple import MQTTClient

#automation import
import irrig_pump_program
import irrig_pump_ctrl
import light_program

#scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()
on_off = OnOffBDC()

#inputs
AI1 = UniversalInput(1, "analog", aic10K)
AI5 = UniversalInput(5, "analog", percentRev)
BI8 = UniversalInput(8, "binary", on_off)

#outputs
BO1 = BinaryOutput(1, "pompe1")
BO2 = BinaryOutput(2, "BO2")
BO3 = BinaryOutput(3, "pompe2")
BO4 = BinaryOutput(4, "BO4")
BO5 = BinaryOutput(5, "light")
BO6 = BinaryOutput(6, "BO6")
BO7 = BinaryOutput(7, "flasher")
BO8 = BinaryOutput(8, "lampe")
#not used
BO1.value = False
BO2.value = False
BO3.value = False
BO4.value = False
BO5.value = False
BO6.value = False
BO7.value = False
BO8.value = False

#variables
irrig_start_time = time.mktime(time.localtime())
irrig_stop_time = irrig_start_time
stop_board = False
counter = 0

#variables for irrigation throuh MQTT
irrig = "Off"; irrig_time = 0

#analog inputs values for filters
last_value_AI1 = AI1.value
last_value_AI5 = AI5.value

#binary inputs compare (if needed)
last_state_BI8 = "Off"

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()
t3 = Timer()

#stops board (...for webrepl...and ftp server...)
def _stop():
    global stop_board
    stop_board = True

#reset board
def _reset():
    import machine
    machine.reset()

def _irrig(v,t):
    global irrig
    global irrig_time
    irrig = v
    irrig_time = t
    if irrig == "On": BO3.value = True; t3.start()
    else: BO3.value = False; t3.stop(); pub_cb('/esp8266/ioboard/countdown', "0")
    #à faire: if irrig == on and irrig_time != ancien irrig_time: t3.stop(); t3.start()
    #ça va bien se faire avec une AV qui garde son ancienne valeur....

#mqtt publish
def pub_cb(top, mess):
    global counter
    try:
        client.publish(top, mess)
        counter = 0
    except:
        counter += 1
        pass

#mqtt subscribe
def sub_cb(topic, msg):
    if topic == b'/esp8266/output/BO2' and 0 <= int(msg) <= True: BO2.value = int(msg)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"Off","time":0}': _irrig("Off", 0)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":2}': _irrig("On", 120)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":5}': _irrig("On", 300)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":15}': _irrig("On", 900)
    if topic == b'/esp8266/system/exit' and msg == b'Exit': _stop()

#mqtt connect and subscribe to Broker
def connect_and_subscribe():
    _client = MQTTClient(hexlify(unique_id()), '192.168.0.149')
    _client.set_callback(sub_cb)
    _client.connect()
    _client.subscribe(b'/esp8266/output/BO2')
    _client.subscribe(b'/esp8266/system/exit')
    _client.subscribe(b'/esp8266/ioboard/valve')
    return _client

#mqtt start
try:
    client = connect_and_subscribe()
except:
    pass

pub_cb('/esp8266/ioboard/countdown', "0")

#main loop execution
while True:
    if stop_board: break
    #analog input filters
    #Present Value = Last Value + (( 100 - Filter ) / 100 * ( Input Value - Last Value ))
    temperature = last_value_AI1 + (0.1 * (AI1.value - last_value_AI1))
    last_value_AI1 = temperature
    photocell = last_value_AI5 + (0.1 * (AI5.value - last_value_AI5))
    last_value_AI5 = photocell

    #automation program for control of irrigation pump BO1
    result = irrig_pump_program.execute(BI8.value, BO1.value, last_state_BI8, irrig_start_time, irrig_stop_time, 1)
    BO1.value = result[0]; last_state_BI8 = result[1]; irrig_start_time = result[2]; irrig_stop_time = result[3]

    #automation program for irrigation pump BO3 through MQTT
    if t3.running() and t3.changed(60): pub_cb('/esp8266/ioboard/countdown', str((irrig_time - t3.elapsed())/60))
    if t3.running() and (irrig_time - t3.elapsed()) <= 0: t3.stop(); BO3.value = False; irrig = "Off"

    #automation program for light control on based on schedule
    result = light_program.execute(time.localtime(), 0600, 1830)
    BO5.value = result
    result = light_program.execute(time.localtime(), 2000, 2200)
    BO8.value = result

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO7.value = not BO7.value
        timer_1 = time.ticks_ms()

    #sync time every hour
    if (time.time() - timer_2) >= 3600:
        import network_rtc
        network_rtc.set_time()
        timer_2 = time.time()

    #mqtt check for messages
    try:
        client.check_msg()
    except:
        pass

    #mqtt reconnect after 5 minutes of each tries OR reset board after 60 minutes
    if counter%5 == 0 and counter != 0:
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
        irrig_obj = {"esp8266 value": BO1.value, "start": irrig_start, "stop": irrig_stop}
        irrig_json = ujson.dumps(irrig_obj)
        board = {"AI1":temperature, "AI5":photocell, "BO1":BO1.value, "BO2":BO2.value, "BO3":BO3.value, "BO4":BO4.value,
                 "BO5":BO5.value, "BO6":BO6.value, "BO7":BO7.value, "BO8":BO8.value, "counter":counter, "board":"esp8266"}

        pub_cb('/esp8266/ioboard/rtc_time', "esp8266 " + date_str+" "+time_str)
        pub_cb('/esp8266/ioboard/irrigation', irrig_json)
        pub_cb('/esp8266/ioboard/in_out', ujson.dumps(board))
        if not t3.running(): pub_cb('/esp8266/ioboard/countdown', "0")

        scan_time = time.ticks_ms()

#Fin
