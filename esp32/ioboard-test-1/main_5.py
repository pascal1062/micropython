#machine import
import time
import sys
import ujson
from universal_input import UniversalInput
from universal_output import UniversalOutput
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from on_off_bdc import OnOffBDC

#mqtt import
import mqtt_client

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
run = False

#analog inputs values for filters
last_value_AI1 = 1024 / 2
last_value_AI4 = 1024 / 2

#binary inputs compare (if needed)
last_state_BI8 = "Off"

#scan rate time (if needed)
scan_time = time.ticks_ms()
mqtt_scan = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()

##mqtt client
mqtt_cl = mqtt_client.mqtt_connect()
topic_sub_1 = b'/output/BO2'
topic_sub_2 = b'/system/exit'


def mqtt_callback(topic, msg):
    if topic == topic_sub_1 and 0 <= int(msg) <= 255: BO2.value = int(msg)
    if topic == topic_sub_2 and run:
        sys.exit()
        import gc
        gc.collect()

mqtt_cl.set_callback(mqtt_callback)
mqtt_cl.subscribe(topic_sub_1)
mqtt_cl.subscribe(topic_sub_2)


#main loop execution
while True:
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

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 500:
        BO8.value = 255 if BO8.value == 0 else 0
        timer_1 = time.ticks_ms()

    #timed loops
    if time.ticks_diff(time.ticks_ms(), scan_time) > 30000:
        #print(temperature, photocell)
        mqtt_cl.publish('input/temperature', str(temperature))
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
        mqtt_cl.publish('ioboard/rtc_time', date_str+" "+time_str)
        irrig_start = time.localtime(irrig_start_time)
        irrig_stop = time.localtime(irrig_stop_time)
        irrig_obj = {"value": BO1.value, "start": irrig_start, "stop": irrig_stop}
        irrig_json = ujson.dumps(irrig_obj)
        mqtt_cl.publish('ioboard/irrigation', irrig_json)
        #try:
            #mqtt_cl.publish('input/temperature', str(temperature))
            #mqtt_cl.publish('ioboard/rtc_time', date_str+" "+time_str)
            #mqtt_cl.publish('ioboard/irrigation', irrig_json)
        #except:
            #continue
        #print(date_str+" "+time_str)
        #print(irrig_json)

        scan_time = time.ticks_ms()

    #mqtt check message every seconds
    if time.ticks_diff(time.ticks_ms(), mqtt_scan) > 1000:
        mqtt_cl.check_msg()
        mqtt_scan = time.ticks_ms()
        run = True

#Fin
