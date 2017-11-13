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

def timerthread(message):
    print 'Timeout, resending the packet'
    # So, must resend the packet
    # must recalculate the checksum
    pkt = 'pkt' + message[:1]
    print 'Sending ' + pkt
    s.sendto(message, (host, port))

# if just sent pkt0 and received ack1, send pkt0 again

msg = raw_input('Enter message to send: ')
counter = 0
currSeq = 0;
lastAck = ''
while(1) :
    # original message
    og = msg

    try :
        checksum = ip_checksum(msg);
        # for invalid checksum
        actualCheck = ip_checksum(msg)
        # if counter == 1:
        #     checksum = ip_checksum("JOKED")
        # print 'Checksum: ' + checksum

        # Set the whole string
        msg = str(currSeq) + str(checksum) + msg
        actualMsg = str(currSeq) + str(actualCheck) + og
        s.sendto(msg, (host, port))

        pkt = 'pkt' + str(currSeq)
        print 'Sending ' + pkt

        # start the timer
        t = threading.Timer(3.0, timerthread, [actualMsg])
        t.start()

        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print 'Server reply: ' + reply

        lastAck = reply[3:]

        # cancel once the ACK has been received
        t.cancel()

        # account for the last ACK that was received

        # if currSeq != int(lastAck):
        #     print 'Mismatched'

        if currSeq == 0 and lastAck == '0':
            currSeq = 1
        elif currSeq == 0 and lastAck == '1':
            currSeq = 0
        elif currSeq == 1 and lastAck == '1':
            currSeq = 0
        elif currSeq == 1 and lastAck == '0':
            currSeq = 1
        else:
            print 'Didnt go in any'
            exit(1)

        time.sleep(2)
        counter += 1
        if counter == 5:
            exit(1)

    except socket.error, msg:
        print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
