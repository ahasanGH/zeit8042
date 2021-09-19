# zeit8042 - Shellcode Design to Buffer Overflow on Windows 7 Machine using vulnerable application as SLMail. 
What we try to achieve?
•	Get the control of EIP register.
•	Tell instruction register to execute our preferred program like /bin/sh, reverse shell, shellcode execution.
•	Or point to the exact memory location where it can execute code or program.
How we do it?
1.	Spiking: Find a vulnerable program or code or application which can use to start exploiting the system and get help of the resources. In our case it is SLmail 5.5: POP3 which is unauthenticated buffer overflow vulnerability exist according to exploit database CVE 2003-0264.
2.	Fuzzing: Try to find out whether the application could be exploited or not? In our case we send a bunch of ‘A’ characters to the application to see (using Immunity Debugger) if we can overrun the ESP | EBP | EIP registers.
3.	Determine the offset of the register: Try to find out the exact position EIP register: means find out the exact memory address of EIP, that can make demarcation point between buffer and EIP | EBP | ESP register. In our case, we use Metasploit-framework (pattern_create.rb | pattern_offset.rb) tools.
4.	Take control of the EIP register: Overwriting the EIP register with the address of the exploitable application or shellcode.
5.	Finding the Bad Characters: List of unwanted characters that can break the shellcode. In SLmail application we found \x00, \x0A, \x0D bad characters.
6.	Finding the right module: Try to find out .DLL or something similar that has no memory protection or could be exploitable. In our case we found SKmail.dll and we try to find an address of an instruction like JMP ESP. Later, stack pointer points to shellcode or other application like /bin/sh or get the reuse shell of the attacked system.
7.	Generate the shellcode (when DEP is disabled): Execute the code to get reverse shell of the attacked system. In our case we use msfvenom tools to generate shellcode.
8.	Generate the ROP Chains (when DEP enabled): 














Youtube Link: https://www.youtube.com/watch?v=j-K0jX0vgkI&ab_channel=AhasanAnowar
