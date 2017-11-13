import socket
import sys
from thread import *

HOST = '' # means all available interfaces
PORT = 2887 #0887 + 2000

# opens a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to avoid port reuse problem
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

try:
    # binds to the host and the port
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# if 10 connections are waiting to be processed, then the 11th connection will be rejected
s.listen(10)
print 'The socket is listening'

# list of all clients
clients = []

# handles connections, creates threads
def clientthread(conn):
    # sending message to connected client
    conn.send('Welcome to the server! Type something and hit enter\n')

    # infinite loop so thread doesn't end
    while True:
        # receiving from client
        data = conn.recv(1024)

        # if "!q" then close the connection with the client
        if data[0:2] == "!q":
            print 'Closing connection'
            for member in clients:
                if conn == member:
                    print 'removing from list'
                    # del member
                    clients.remove(member)
            break

        # for sending to all clients that are connected to server
        if data[0:9] == "!sendall ":
            print 'Sending to all clients'

            # allReply has the stuff after !sendall
            allReply = data[9:]
            # iterates through all the clients
            for member in clients:
                member.sendall(allReply)

        reply = 'OK...' + data
        if not data:
            break
        conn.sendall(reply)

    # exited loop
    conn.close()

while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()

    #display the client information
    print 'Connected with ' + addr[0] + ': ' + str(addr[1])
    clients.append(conn)

    # starting new thread
    start_new_thread(clientthread, (conn, ))

    # try to keep talking with the client
    # data = conn.recv(1024)
    # reply = 'OK...' + data
    # if not data:
        # break

    # conn.sendall(reply)

conn.close()
s.close()
