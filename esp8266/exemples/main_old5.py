#machine import
import time
import ujson
from ai import AnalogInput
from bi import BinaryInput
from bo import BinaryOutput
from av import AnalogValue
from bv import BinaryValue
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from timer import Timer

#mqtt import
from ubinascii import hexlify
from machine import unique_id
from umqtt.simple import MQTTClient

#automation import
import light_program

#scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()

#inputs
AI1 = AnalogInput(1, "temp", 80, aic10K)
BI2 = BinaryInput(2, "etat-relais")
AI5 = AnalogInput(5, "photocell", 80, percentRev)
BI8 = BinaryInput(8, "bouton")

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
stop_board = BinaryValue(1, "stop-board")
counter = AnalogValue(1, "compteur")

#variables for irrigation throuh MQTT
irrig = BinaryValue(2, "irrigation_start")
irrig_time = AnalogValue(2, "irrigation_time")

#first scan
AI1.value; AI5.value

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()
timer_2 = time.time()
t1 = Timer()
t3 = Timer()

#reset board
def _reset():
    import machine
    machine.reset()

def _irrig(v,t):
    irrig.value = v
    irrig_time.value = t
    if irrig.value: BO3.value = True; t3.stop(); t3.start()
    else: BO3.value = False; t3.stop(); pub_cb('/esp8266/ioboard/countdown', "0")

#mqtt publish
def pub_cb(top, mess):
    try:
        client.publish(top, mess)
        counter.value = 0
    except:
        counter.value += 1
        pass

#mqtt subscribe
def sub_cb(topic, msg):
    if topic == b'/esp8266/output/BO2': BO2.value = True if msg == "255" else False
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"Off","time":0}': _irrig(False, 0)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":2}': _irrig(True, 120)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":5}': _irrig(True, 300)
    if topic == b'/esp8266/ioboard/valve' and msg == b'{"trig":"On","time":15}': _irrig(True, 900)
    if topic == b'/esp8266/system/exit' and msg == b'Exit': stop_board.value = True

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
    #logger = open("logger.txt","a"); logger.write(str(time.localtime()) + " except line 114\n"); logger.close()
    pass

pub_cb('/esp8266/ioboard/countdown', "0")

#main loop execution
while True:
    if stop_board.value: break

    #Inputs miscellanous
    temperature = AI1.value; photocell = AI5.value
    BI2.value; BI8.value

    #automation program for control of irrigation pump BO1
    if t1.running() and (t1.elapsed() >= 60): t1.stop(); BO1.value = False
    if BI8.rising(): BO1.value = True; t1.stop(); t1.start()

    #automation program for irrigation pump BO3 through MQTT
    if t3.running() and t3.changed(60): pub_cb('/esp8266/ioboard/countdown', str((irrig_time.value - t3.elapsed())/60))
    if t3.running() and (irrig_time.value - t3.elapsed()) <= 0: t3.stop(); BO3.value = False; irrig.value = False
    if BI2.changed(): pub_cb('/esp8266/ioboard/relay', str(BI2.value))

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

    #mqtt reconnect after 15 minutes of each tries OR reset board after 60 minutes
    #if counter.value %15 == 0 and counter.value != 0:
    #    try:
    #        client = connect_and_subscribe()
    #    except:
    #        #logger = open("logger.txt","a"); logger.write(str(time.localtime()) + " except line 164, counter = " + str(counter.value) + "\n"); logger.close()
    #        pass
    #if counter.value >= 60: _reset()

    #mqtt publish (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 60000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        board = {"AI1":temperature, "AI5":photocell, "BO1":BO1.value, "BO2":BO2.value, "BO3":BO3.value, "BO4":BO4.value,
                 "BO5":BO5.value, "BO6":BO6.value, "BO7":BO7.value, "BO8":BO8.value, "counter":counter.value, "board":"esp8266"}

        pub_cb('/esp8266/ioboard/rtc_time', "esp8266 " + date_str+" "+time_str)
        pub_cb('/esp8266/ioboard/in_out', ujson.dumps(board))
        if not t3.running(): pub_cb('/esp8266/ioboard/countdown', "0")

        scan_time = time.ticks_ms()

#Fin
