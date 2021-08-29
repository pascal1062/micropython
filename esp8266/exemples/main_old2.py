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
BO1 = UniversalOutput(1, "binary")
BO2 = UniversalOutput(2, "binary")
BO3 = UniversalOutput(3, "binary")
BO4 = UniversalOutput(4, "binary")
BO5 = UniversalOutput(5, "binary")
BO6 = UniversalOutput(6, "binary")
BO7 = UniversalOutput(7, "binary")
BO8 = UniversalOutput(8, "binary")
#not used
BO1.value = 0
BO2.value = 0
BO3.value = 0
BO4.value = 0
BO5.value = 0
BO6.value = 0
BO7.value = 0
BO8.value = 0

#variables
irrig_start_time = time.mktime(time.localtime())
irrig_stop_time = irrig_start_time
stop_board = False
counter = 0

#variables for irrigation throuh MQTT
irrig = "Off"; irrig_flag = "Off"; irrig_time = 0; irrig_time_I = 0;  irrig_time_O = 0; irrig_time_L = 0

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

#stops board (...for webrepl...and ftp server...)
def _stop():
    global stop_board
    stop_board = True

#reset board
def _reset():
    import machine
    machine.reset()

def _irrig(v, t):
    global irrig
    global irrig_time
    irrig = v
    irrig_time = t
    try:
        client.publish('/esp8266/ioboard/countdown', str(round(irrig_time)))
    except:
        pass

#mqtt client
def sub_cb(topic, msg):
    if topic == b'/esp8266/output/BO2' and 0 <= int(msg) <= 255: BO2.value = int(msg)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"Off","time":0}': _irrig("Off", 0)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":2}': _irrig("On", 2)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":5}': _irrig("On", 5)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":15}': _irrig("On", 15)
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
    result = irrig_pump_ctrl.execute(BO3.value, irrig, irrig_flag, irrig_time_I, irrig_time_O, irrig_time)
    BO3.value = result[0]; irrig = result[1]; irrig_flag = result[2]; irrig_time_I = result[3]; irrig_time_O = result[4]; irrig_time_L = result[5]
    #if irrig != irrig_flag:
    #    if (irrig == "On") and (BO3.value == 0): BO3.value = 255; irrig_time_I = time.time(); irrig_time_O = irrig_time_I + irrig_time
    #    if irrig == "Off": BO3.value = 0; irrig_time_I = 0; irrig_time_O = 0
    #irrig_flag = irrig
    #if (time.time() >= irrig_time_O) and (irrig_time_O != 0) and (BO3.value == 255): BO3.value = 0; irrig_time_I = 0;  irrig_time_O = 0
    #irrig_time_L = (irrig_time_O - time.time()) / 60  if (BO3.value == 255) else 0

    #automation program for light control on based on schedule
    result = light_program.execute(time.localtime(), 0600, 1830)
    BO5.value = result
    result = light_program.execute(time.localtime(), 2000, 2200)
    BO8.value = result

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO7.value = 255 if BO7.value == 0 else 0
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

        try:
            client.publish('/esp8266/ioboard/rtc_time', "esp8266 " + date_str+" "+time_str)
            client.publish('/esp8266/ioboard/irrigation', irrig_json)
            client.publish('/esp8266/ioboard/in_out', ujson.dumps(board))
            client.publish('/esp8266/ioboard/countdown', str(round(irrig_time_L, 1)))
            counter = 0
        except:
            counter += 1
            pass

        scan_time = time.ticks_ms()

#Fin
