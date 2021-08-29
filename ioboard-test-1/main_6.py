#machine import
import time
import ujson
from universal_input import UniversalInput
from universal_output import UniversalOutput
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from on_off_bdc import OnOffBDC

#modbus TCP import
from uModBus.tcp import TCPServer

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

#analog inputs values for filters
last_value_AI1 = 1024 / 2
last_value_AI4 = 1024 / 2

#binary inputs compare (if needed)
last_state_BI8 = "Off"

#scan rate time (if needed)
scan_time = time.ticks_ms()

#miscellanous timers
timer_1 = time.ticks_ms()

#start modbus TCP server and bind it to local esp32 IP address and port
modbus_tcp = TCPServer()
modbus_tcp.bind('192.168.0.124', 10502)

#modbus responses buffer lists
date_time = [time.localtime()[0], time.localtime()[1], time.localtime()[2], time.localtime()[3], time.localtime()[4], time.localtime()[5]] #IR0 to IR5
inputs = [round(round(AI1.value,2)*100), 0, 0, round(round(AI4.value,2)*100), 0, 0, 0, 0] #IR10 to IR17
outputs = [BO1.value, BO2.value, BO3.value, BO4.value, BO5.value, BO6.value, BO7.value, BO8.value] #HR0 to HR7

#send modbus response
def modbus_resp(req):
    #FC3 or FC4 or FC16
    if req[1] == 4 and req[3] == 0: modbus_tcp.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None, date_time)
    if req[1] == 4 and req[3] == 10: modbus_tcp.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None, inputs)
    if req[1] == 3 and req[3] == 0: modbus_tcp.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None, outputs)
    if req[1] == 16: modbus_tcp.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None)
    if req[1] == 16: BO4.value = req[8]



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

    #modbus TCP check messages. unitID=1, timeout=0
    #received examples: b'\x01\x04\x00\x00\x00\x06'
    #                   b'\x01\x03\x00\x00\x00\x08'
    #                   b'\x01\x10\x00\x00\x00\x00\x01\x00'  write
    mrequest = modbus_tcp.get_request([1],0)
    if mrequest is not None:
        print(mrequest)
        modbus_resp(mrequest)

    #timed loops
    if time.ticks_diff(time.ticks_ms(), scan_time) > 5000:
        date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
        time_str = "{:02}:{:02}:{:02}".format(time.localtime()[3], time.localtime()[4], time.localtime()[5])

        irrig_start = time.localtime(irrig_start_time)
        irrig_stop = time.localtime(irrig_stop_time)
        irrig_obj = {"value": BO1.value, "start": irrig_start, "stop": irrig_stop}
        irrig_json = ujson.dumps(irrig_obj)

        #modbus lists update
        date_time = [time.localtime()[0], time.localtime()[1], time.localtime()[2], time.localtime()[3], time.localtime()[4], time.localtime()[5]] #IR0 to IR5
        inputs = [round(round(temperature,2)*100), 0, 0, round(round(photocell,2)*100), 0, 0, 0, 0] #IR10 to IR17
        outputs = [BO1.value, BO2.value, BO3.value, BO4.value, BO5.value, BO6.value, BO7.value, BO8.value] #HR0 to HR7

        #print(date_str+" "+time_str)
        #print(irrig_json)

        scan_time = time.ticks_ms()

#Fin
