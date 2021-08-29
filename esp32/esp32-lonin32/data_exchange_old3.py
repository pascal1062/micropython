import socket
import select

class DataExchange():

    def __init__(self):
        self._local_ip = None
        self._port = 0
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._poller = select.poll()
        self._data = None

    def attach(self, local_IP, port=47902):
        self._local_ip = local_IP
        self._port = port
        self._sock.bind((self._local_ip, self._port))
        self._sock.setblocking(False)
        self._poller.register(self._sock, select.POLLIN)

    def detach(self):
        self._sock.close()

    def recv_data(self):
        while True:
            self._data = None
            res = self._poller.poll(1)
            if res:
                if res[0][1] & select.POLLIN:
                    self._data = self._sock.recv(128)
                    try:
                        msg = self._data.decode("utf-8")
                        msg_list = msg.split("-")
                        if len(msg_list) == 2: return msg_list
                    except:
                        return None
                    break
            return None
            break

    def send_data(self, message, server_addr, port=47902):
        self._sock.sendto(message, (server_addr, port))                 

#Fin