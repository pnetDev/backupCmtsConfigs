#!/usr/bin/python

HOST = "10.1.1.116"
PORT = 23
TIMEOUT = 3
PASSWD = "hsds"
COMMANDS = ["hsds","en","hsds","copy start tftp://10.1.1.51/labBsrCmts.cfg","",""]

import telnetlib

tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
#tn.set_debuglevel(1)
tn.write("\r\n\r\n")
for cmd in COMMANDS:
    tn.write(cmd+"\r\n")

print tn.read_until("#\r\n",3)

tn.close()
