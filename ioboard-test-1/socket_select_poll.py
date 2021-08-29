import time
import socket
import uselect as select

server = socket.socket()
server.bind(('192.168.0.124', 10503))
server.setblocking(False)
server.listen(1)
message_queues = {}

poller = select.poll()
poller.register(server, select.POLLOUT | select.POLLIN)
fd_to_socket = { server.fileno(): server }

while True:
    events = poller.poll(10000)

    for fd, flag in events:
        s = fd_to_socket[fd]
        if flag & select.POLLIN:
            if s is server:
                connection, client_address = s.accept()
                print("new connection from " + client_address)
                connection.setblocking(0)
                fd_to_socket[ connection.fileno() ] = connection
                poller.register(connection, (select.POLLIN | select.POLLHUP | select.POLLERR))
                message_queues[connection] = Queue.Queue()
            else
                data = s.recv(128)

                if data:
                    print("data received: " + data)
                    message_queues[s].put(data)
                    poller.modify(s, select.POLLOUT | select.POLLIN)
                else
                    print("closing " + client_address + " after reading data")
                    poller.unregister(s)
                    s.close()

                    del message_queues[s]

        elif flag & select.POLLOUT:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                # No messages waiting so stop checking for writability.
                print("Error empty")
                poller.modify(s, (select.POLLIN | select.POLLHUP | select.POLLERR))
            else:
                print("sending... ")
                s.send(next_msg)
        elif flag & select.POLLERR:
            print("Error POLLERR")
            # Stop listening for input on the connection
            poller.unregister(s)
            s.close()

            # Remove message queue
            del message_queues[s]
