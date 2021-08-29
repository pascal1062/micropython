import time
import machine
from umqtt.robust import MQTTClient
from universal_output import UniversalOutput

BO8 = UniversalOutput(8, "binary")
timer_1 = time.ticks_ms()
mqtt_run = True

timer = machine.Timer(0)

def watch_dog(timer):
    c.disconnect()
    mqtt_run = False
    print("mqtt stopped")

def sub_cb(topic, msg):
    timer.init(period=2000, mode=machine.Timer.PERIODIC, callback=watch_dog)
    print((topic, msg))
    timer.deinit()
    #if msg == "mqtt reconnect: OSError(104,) ": machine.reset()
    #if type(msg) is str: machine.reset()



c = MQTTClient("umqtt_client", "192.168.0.149")
# Print diagnostic messages when retries/reconnects happens
c.DEBUG = True
c.set_callback(sub_cb)
# Connect to server, requesting not to clean session for this
# client. If there was no existing session (False return value
# from connect() method), we perform the initial setup of client
# session - subscribe to needed topics. Afterwards, these
# subscriptions will be stored server-side, and will be persistent,
# (as we use clean_session=False).
#
# There can be a problem when a session for a given client exists,
# but doesn't have subscriptions a particular application expects.
# In this case, a session needs to be cleaned first. See
# example_reset_session.py for an obvious way how to do that.
#
# In an actual application, it's up to its developer how to
# manage these issues. One extreme is to have external "provisioning"
# phase, where initial session setup, and any further management of
# a session, is done by external tools. This allows to save resources
# on a small embedded device. Another extreme is to have an application
# to perform auto-setup (e.g., clean session, then re-create session
# on each restart). This example shows mid-line between these 2
# approaches, where initial setup of session is done by application,
# but if anything goes wrong, there's an external tool to clean session.
if not c.connect(clean_session=False):
    print("New session being set up")
    c.subscribe(b"/output/BO2")

while 1:
    if mqtt_run: c.check_msg()

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO8.value = 255 if BO8.value == 0 else 0
        timer_1 = time.ticks_ms()

c.disconnect()
