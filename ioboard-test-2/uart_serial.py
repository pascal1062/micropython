from machine import UART
import ujson

uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

#json example
{"mode": "read", "object": "object?", "property": "property?", "reply": "yes" }
{"mode": "write", "object": "object?", "value": "xxx", "timer": 60, "reply": "no" }

#examples
{"mode": "read", "object": "temperature", "property": "value", "value": None, "timer": None, "reply": "yes" }
{"mode": "write", "object": "valve", , "property": "value", "value": "start", "timer": 60, "reply": "no" }

#maybe do a dictionnary for keeping the value of the output to write.... ex.
out_1 = {"name": "sortie_1", "value": "Off"}

def uart_receive():
    bytes =  uart.readline()
    if bytes != None:
        try:
            parsed = ujson.loads(bytes)
            mode = parsed["mode"]
            reply = parsed["reply"]
            obj = parsed["object"]
            value = parsed["value"]
            if mode == "read" and reply == "yes": uart_reply(obj)
            if mode == "write": exec_write(obj, value)
        except:
            pass


def exec_write(obj, value):
    out_1["value"] = value
    pass


def uart_reply(obj):
    val = public.temperature.value
    json_str = '{"mode": "reply", "object": "temperature", "value": ' +str(val)+' }'
    uart.write(json_str+'\n')



#End
