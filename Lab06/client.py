import socket #for sockets
import sys  #for exit
import threading
import time # for delays
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;

def timerthread(message):
    print 'Timeout'
    # So, must resend the packet

    print 'Resending the packet'
    s.sendto(message, (host, port))

    # in order to handle multiple threads

msg = raw_input('Enter message to send: ')
counter = 0
currSeq = 0;

numPackets = 12

while(1) :
    # msg = raw_input('Enter message to send: ')
    # msg = packets[counter]
    og = msg

    try :
        checksum = ip_checksum(msg);

        # for invalid checksum
        actualCheck = ip_checksum(msg)
        # if counter == 1:
        #     checksum = ip_checksum("JOKED")
        print 'Checksum: ' + checksum

        # for window of size 4
        for x in range(0, 3):
            pkt = 'pkt' + str(currSeq)
            print 'Sending ' + pkt
            # for first window, have pkt0 - pkt3
            # after sending, then wait
            msg = str(currSeq) + str(checksum) + msg
            actualMsg = str(currSeq) + str(actualCheck) + og
            s.sendto(msg, (host, port))

            # start the timer every time that a pkt is sent
            t = threading.Timer(4.0, timerthread, [actualMsg])
            t.start()

            currSeq += 1

            time.sleep(2)

        # pkt = 'pkt' + str(currSeq)
        # print 'Sending ' + pkt

        # change seq # for the next message
        # if currSeq == 0:
        #     currSeq = 1
        # else :
        #     currSeq = 0

        # once ack is received, then send another pkt
        # but how to send another packet

        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print 'Server reply: ' + reply

        # cancel once the ACK has been received
        t.cancel()

        time.sleep(3)
        counter += 1

    except socket.error, msg:
        print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
