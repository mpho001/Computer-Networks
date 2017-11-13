import socket
import sys
import time

def ip_checksum(data):
    pos = len(data)
    if (pos & 1): # if odd
        pos -= 1
        sum = ord(data[pos])
    else:
        sum = 0

    # loop to calculate the checksums
    while pos > 0:
        pos -= 2
        sum += (ord(data[pos+1]) << 8) + ord(data[pos])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    result = (~ sum) & 0xffff # keep lower 16 bits
    result = result >> 8 | ((result & 0xff) << 8) # swapping bytes
    return chr(result / 256) + chr(result % 256)

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

# Keep talking with the client
# flag for whether it should be 0 or not
# ackFlag = 0

# TO DO
# figure out how to keep track of duplicate packets
# when duplicate packet received, immediately send an ack for that duplicate

counter = 0
prevAck = ''

while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break

    seqNum = data[:1]

    # check the checksum
    # testing = data[3:]
    testCheck = ip_checksum(data[3:])
    checksum = data[1:3];
    # print 'Checksum: ' + testCheck

    # if (testCheck == data[1:3]):
        # print 'The checksums match'
    if (testCheck != data[1:3]):
        print 'The checksums do not match: ' + data[1:3]
        print data[3:]
        time.sleep(2)
        continue
        #while (testCheck != data[1:3]):
        #    print 'Waiting for correct pkt'
        #    time.sleep(2)

    # print 'Seqnum: ' + seqNum
    # if seqNum != ackFlag:
        # print 'Wrong ack'

    # TO DO
    # Send a delayed ack so that the sender sends two pck1
    # but how do i do that
    if seqNum == '0':
        reply = 'ack0'
        print 'Received pck0'
        print 'Sending ack0'
        s.sendto(reply, addr)
    elif seqNum == '1':
        reply = 'ack1'
        print 'Received pck1'
        # print 'Sending ack1'
        if counter == 1:
            time.sleep(4)
        print 'Sending ack1'
        s.sendto(reply, addr)

    # print 'Ack number: ' + counter

    # s.sendto(reply, addr)
    # if counter == 1:
    #     print 'Just sent after delay'
    #     exit(1)

    counter += 1

    # reply = 'OK...' + data

    # s.sendto(reply, addr)
    # print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

    # send ack depending on sequence number
    # sequence number is first character of the received message

s.close()
