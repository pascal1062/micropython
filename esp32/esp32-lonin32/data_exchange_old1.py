import socket
import select
import ujson


class DataExchange():

    def __init__(self, local_IP, port=47902):
        self._local_ip = local_IP
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._poller = select.poll()
        self._data = None

    def attach(self):
    	self._sock.bind((self._local_ip, self._port))
    	self._sock.setblocking(False)
    	self._poller.register(self._sock, select.POLLIN)

    def detach(self):
    	self._sock.close()

    def decode(self, msg):
    	try:
    		return(ujson.loads(msg))
    	except:
    		return None

    def recv_data(self):
    	while True:
    		#self._data = None
            self._data = {} #empty list
    		res = self._poller.poll(1)
    		if res:
    			if res[0][1] & select.POLLIN:
    				self._data = self._sock.recv(128)
    				try:
    					return ujson.loads(self._data)
    				except:
    					pass
    				break

    		break

    def send_data(self, message, server_addr, port=47903):
    	self._sock.sendto(message, (server_addr, port))	    			

#Fin