from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
from random import randint
from universal_output import UniversalOutput
import micropython

#àfaire
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
CLIENT_ID = CLIENT_ID + str(randint(0,65535))

# ESP8266 ESP-12 modules have blue, active-low LED on GPIO2, replace
# with something else if needed.
#led = Pin(2, Pin.OUT, value=1)
BO6 = UniversalOutput(6, "binary")

# Default MQTT server to connect to
SERVER = "192.168.0.149"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
#TOPIC = b"led"
TOPIC = "/output/BO2"

state = 0

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == 255:
        BO6.value = 255
        state = 1
    elif msg == 0:
        BO6.value = 0
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state    c.connect()    c.connect()
        # value will make it toggle
        #led.value(state)
        state = 1 - state


def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.connect()
    c.set_callback(sub_cb)
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    #try:
    #    while 1:
            #micropython.mem_info()
    #        c.check_msg()
    #finally:
    #    c.disconnect()

    while 1:
        try:
            c.check_msg()
        except:
            #c.disconnect()
            print("disconnected")

main()
