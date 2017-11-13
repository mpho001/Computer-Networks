import socket
import sys
import time
from check import ip_checksum

def makeAck(seqNum):
    ack = 'ACK' + seqNum
    return ack

HOST = ''
PORT = 8888

# Datagram (UDP socket)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code: ' +str(msg[0])+ ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST,PORT))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

expectedSeqNum = 1

# Keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break

    seqNum = data[:1]

    if (seqNum != expectedSeqNum):
        print 'Pkt out of order'
        newAck = int(seqNum) + 1
        makeAck(str(newAck))
        continue

    # check the checksum
    # testing = data[3:]
    testCheck = ip_checksum(data[3:])
    checksum = data[1:3];
    print 'Checksum: ' + testCheck

    if (testCheck == data[1:3]):
        print 'The checksums match'
    else:
        print 'The checksums do not match: ' + data[1:3]
        print data[3:]
        time.sleep(2)
        continue

    ack = makeAck(seqNum)
    s.sendto(ack, addr)

    expectedSeqNum += 1

    # if seqNum == '0':
    #     reply = 'ack0'
    #     print 'Received pck0'
    #     print 'Sending ack0'
    # elif seqNum == '1':
    #     reply = 'ack1'
    #     print 'Received pck1'
    #     print 'Sending ack1'

    # s.sendto(reply, addr)

s.close()
