#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.255', 88))
s.send('Fuck You Faggot')
data = s.recv(1024)
s.close()
print 'Received: '
print data
