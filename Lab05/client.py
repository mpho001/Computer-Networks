import socket #for sockets
import sys  #for exit
import threading
import time # for delays

def ip_checksum(data):
    pos = len(data)
    if (pos & 1):
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

    result = (~ sum) & 0xffff
    result = result >> 8 | ((result & 0xff) << 8)
    return chr(result / 256) + chr(result % 256)


# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;

# checksum = ip_checksum('Melinda')
# print checksum

# the current sequence number

# after sending pkt, wait until receiver sends an ack

packets = ["pkt0", "pk1", "pkt0"]
counter = 0

msg = raw_input('Enter message to send: ')

def timerthread(message):
    print 'Timeout'
    # So, must resend the packet
    # must recalculate the checksum
    print 'Resending the packet'
    # pkt = message[:1]
    # print 'Sending ' + pkt
    s.sendto(message, (host, port))

currSeq = 0;
while(1) :
    # msg = raw_input('Enter message to send: ')
    # msg = packets[counter]
    og = msg

    try :
        checksum = ip_checksum(msg);
        # for second part, invalid checksum
        actualCheck = ip_checksum(msg)
        if counter == 1:
            checksum = ip_checksum("JOKED")

        #Set the whole string
        msg = str(currSeq) + str(checksum) + msg
        actualMsg = str(currSeq) + str(actualCheck) + og
        s.sendto(msg, (host, port))

        pkt = 'pkt' + str(currSeq)
        print 'Sending ' + pkt

        # start the timer
        t = threading.Timer(2.0, timerthread, [actualMsg])
        t.start()

        # change seq # for the next message
        if currSeq == 0:
            currSeq = 1
        else :
            currSeq = 0

        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print 'Server reply: ' + reply

        # cancel once the ACK has been received
        t.cancel()

        time.sleep(3)
        counter += 1

        if counter == 3:
            exit(1)

    except socket.error, msg:
        print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
