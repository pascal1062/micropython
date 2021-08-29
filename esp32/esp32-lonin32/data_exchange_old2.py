import socket
import select
import ujson


class DataExchange():

	def __init__(self):
		self._local_ip = None
		self._port = 0
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._poller = select.poll()
		self._data = None
		self._board = None

	def attach(self, board, local_IP, port=47902):
		self._local_ip = local_IP
		self._port = port
		self._board = board
		self._sock.bind((self._local_ip, self._port))
		self._sock.setblocking(False)
		self._poller.register(self._sock, select.POLLIN)

	def detach(self):
		self._sock.close()

	def _decode(self, msg_bytes):
		json_msg = None
		keys = []
		values = []
		json_val = {}
		try:
			json_msg = ujson.loads(msg_bytes)
			for key, value in json_msg.items():
				keys.append(key)
				values.append(value)

			json_val.update({keys[1]: values[1]}) 
			if json_msg['board'] == self._board: return json_val
		except:
			pass    

	def recv_data(self):
		while True:
			#self._data = None
			self._data = {} #empty list
			res = self._poller.poll(1)
			if res:
				if res[0][1] & select.POLLIN:
					self._data = self._sock.recv(128)
					#return self._decode(self._data)
					#ici ça marche pas.....on essai ça ici plus bas
					try:
						json_msg = ujson.loads(self._data)
						if json_msg['board'] == self._board: return json_msg
					break
			break

	def send_data(self, message, server_addr, port=47903):
		self._sock.sendto(message, (server_addr, port))	    			

#Fin

'''
  txt = b'/lonin32/exit-True'
  stg = txt.decode("utf-8")
  x = stg.split("-")
'''