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
import light_program

#scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()
on_off = OnOffBDC()

#inputs
AI1 = UniversalInput(1, "analog", percentRev)
AI3 = UniversalInput(3, "analog", aic10K)
#BI3 = UniversalInput(3, "binary", on_off)
BI8 = UniversalInput(8, "binary", on_off)

#outputs
BO1 = UniversalOutput(1, "binary")
BO2 = UniversalOutput(2, "binary")
BO3 = UniversalOutput(3, "binary")
BO4 = UniversalOutput(4, "binary")
#not used
BO1.value = 0
BO2.value = 0
BO3.value = 0
BO4.value = 0

#variables
stop_board = False

#analog inputs values for filters
last_value_AI1 = 50
last_value_AI3 = 20

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()


#main loop execution
while True:
    if BI8.value == 'Off': break

    #analog input filters
    #Present Value = Last Value + (( 100 - Filter ) / 100 * ( Input Value - Last Value ))
    photocell = last_value_AI1 + (0.1 * (AI1.value - last_value_AI1))
    last_value_AI1 = photocell
    temperature = last_value_AI3 + (0.1 * (AI3.value - last_value_AI3))
    last_value_AI3 = temperature

    if photocell < 20: BO2.value = 255
    if photocell > 60: BO2.value = 0

    #BO3.value = 255 if BI3.value == 'On' else 0

    #automation program for light control on based on schedule
    result = light_program.execute(time.localtime(), 0600, 1900)
    BO1.value = result

    #led flasher light_program
    if time.ticks_diff(time.ticks_ms(), timer_1) > 200:
        BO4.value = 255 if BO4.value == 0 else 0
        timer_1 = time.ticks_ms()

    #print to file every 5 minutes
    #if time.ticks_diff(time.ticks_ms(), scan_time) > 300000:
    #    date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
    #    time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])
    #    date_time = date_str +" "+ time_str
    #    f = open('data.txt', 'a')
    #    f.seek(0, 2)
    #    f.write(date_time+ ", "+ str(AI3.value))
    #    f.write('\n')
    #    f.close()
    #    scan_time = time.ticks_ms()

#Fin
