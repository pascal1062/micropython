
from uModBus.tcp import TCPServer

modbus_obj = TCPServer()
modbus_obj.bind('192.168.0.124', 10502)


while 1:
    req = modbus_obj.get_request([1],0)
    if req != None: modbus_obj.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None, [1,2,3])


#response for READ HOLDING REGISTERS or READ INPUT REGISTERS
modbus_obj.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None, [1,2,3])

#response for WRITE HOLDING REGISTERS
modbus_obj.send_response(req[0], req[1], req[2]+req[3], req[4]+req[5], None)
