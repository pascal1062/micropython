
def emergency():
    import socket
    import select

    addr = ('192.168.0.149', 47901)

    s = socket.socket()
    s.setblocking(False)
    message = "Default"

    try:
        s.connect(addr)
    except OSError:
        pass

    poller = select.poll()
    poller.register(s, select.POLLIN)

    #i = 0
    while True:
        #i+=1
        #if i >= 5: break
        res = poller.poll(1000)
        if res:
            #if res[0][1] & select.POLLOUT:
            #    try:
            #        s.send(b"mqtt server connection lost\n")
            #    except:
            #        pass
            #    poller.modify(s,select.POLLIN)
            #    continue
            if res[0][1] & select.POLLIN:
                try:
                    message = s.recv(20)
                except:
                    pass
                break
        break

    s.close()

    return message

#End
import socket
udp = "192.168.0.55"
port = 47902
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((udp, port))
s.settimeout(0.01)

while True:
    try:
        data = s.recv(1024)
        print(data)
    except:
        print("Hello")    
        pass

s.sendto(MESSAGE, (UDP_IP, UDP_PORT))  

 
_server = ("192.168.0.149", 47904)
p = 2000

 def _poll3():
        while True:
...         res = poller.poll(2000)
...         poller.modify(s,select.POLLOUT)
...         if res:
...             if res[0][1] & select.POLLOUT:
...                 s.sendto("MESSAGE", ("192.168.0.149", 47904))
...                 poller.modify(s,select.POLLIN)
...                 continue
...             if res[0][1] & select.POLLIN:    
...                 print(s.recv(128))
...                 break
...         break 
    