import socket
import sys # for exit

# AF_INET = IPv4
# SOCK_STREAM = TCP

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket Created'

# host = 'www.wikipedia.org'
host = 'www.google.com'
port = 80 # 0887 + 2000

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    # could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'IP address of ' + host + ' is ' + remote_ip

s.connect((remote_ip, port))

print 'Socket Connected to ' + host + ' on IP ' + remote_ip

# send data to remote server
message = "GET / HTTP/1.1\r\n\r\n"

try:
    # set the whole string
    s.sendall(message)
except socket.error:
    # the send failed!!! D:
    print 'Send failed ):'
    sys.exit()

print 'The message sent successfully!'

# receiving the data!!
reply = s.recv(4096)
print reply

s.close()
