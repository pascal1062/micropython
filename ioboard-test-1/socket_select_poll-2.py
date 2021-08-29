import usocket as socket
import uselect as select

def do_something_else():
    print("something else")
    #The other script to be executed besides of the blocking socket

def Client_handler(client_obj):
    pass #Do this when there's a socket connection

server = socket.socket()
server.bind(('192.168.0.124', 10503))
server.setblocking(False)
server.listen(5)

poller = select.poll()
poller.register(server, select.POLLOUT | select.POLLIN)

while True:
    res = poller.poll(10000)
    if res:
        if res[0][1] & select.POLLOUT:
            print("Doing Handshake")
            server.do_handshake()
            print("Handshake Done")
            server.send(b"GET / HTTP/1.0\r\n\r\n")
            poller.modify(server,select.POLLIN)
            continue
        if res[0][1] & select.POLLIN:
            print(server.recv(4092))
            break
    break

"""
while True:
    events = poller.poll(100)
    print('events =', events)
    for file in events:
        # file is a tuple
        if file:
            ch = server.recv(25)
            print('Got ', ch)

#    while True:
#        r, w, err = select.select((server,), (), (), 1)
#        if r:
#            for readable in r:
#                client, client_addr = server.accept()
#                try:
#                    Client_handler(client)
#                except OSError as e:
#                    pass
#        do_something_else()

"""

#End
