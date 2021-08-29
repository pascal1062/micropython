#machine import
import time
import ujson
from machine import Pin

from av import AnalogValue
from bv import BinaryValue

#mqtt import
from ubinascii import hexlify
from machine import unique_id
from umqtt.simple import MQTTClient

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

#mqtt publish
def pub_cb(top, mess):
    try:
        client.publish(top, mess)
        counter.value = 0
    except:
        counter.value += 1
        logger = open("logger.txt","a"); logger.write(str(time.localtime()) + " except line 39, counter = " + str(counter.value) + "\n"); logger.close()
        pass

#mqtt subscribe
def sub_cb(topic, msg):
    if topic == b'/lonin32/msgin': print(msg)
    if topic == b'/lonin32/system/exit' and msg == b'Exit': stop_board.value = True

#mqtt connect and subscribe to Broker
def connect_and_subscribe():
    _client = MQTTClient(hexlify(unique_id()), '192.168.0.149')
    _client.set_callback(sub_cb)
    _client.connect()
    _client.subscribe(b'/lonin32/msgin')
    _client.subscribe(b'/lonin32/system/exit')
    return _client

#mqtt start
try:
    client = connect_and_subscribe()
except:
    logger = open("logger.txt","a"); logger.write(str(time.localtime()) + " except line 60\n"); logger.close()
    pass

pub_cb('/lonin32/msgout', "0")

#main loop execution
while True:
    if stop_board.value: break

    #sync time every hour
    if (time.time() - timer_2) >= 3600:
        import network_rtc
        network_rtc.set_time()
        timer_2 = time.time()

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        led.value(0) if led.value() == 1 else led.value(1)
        timer_1 = time.ticks_ms()

    #mqtt check for messages
    try:
        client.check_msg()
    except:
        pass

    #mqtt reconnect after 5 minutes of each tries OR reset board after 60 minutes
    if counter.value %5 == 0 and counter.value != 0:
        try:
            connect_and_subscribe()
            #Ici le delai est assez long...plusieurs secondes d'attente quand le réseau est planté...
        except:
            logger = open("logger.txt","a"); logger.write(str(time.localtime()) + " except line 91, counter = " + str(counter.value) + "\n"); logger.close()
            pass
    if counter.value == 60: _reset()

    #mqtt publish (60 secs loop)
    if time.ticks_diff(time.ticks_ms(), scan_time) > 60000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        board = {"counter":counter.value, "board":"lonin32"}

        pub_cb('/lonin32/ioboard/rtc_time', "lonin32 " + date_str+" "+time_str)
        print("lonin32 " + date_str+" "+time_str)

        scan_time = time.ticks_ms()

#Fin
