#!/usr/bin/python

import telnetlib
import datetime

now = datetime.datetime.now()

host = "wmtn4" # your router ip
username = "root" # the username
password = "casa"
filename_prefix = "cisco-backup"

tn = telnetlib.Telnet(host)
tn.read_until("login:")
tn.write(username+"\n")
tn.read_until("Password:")
tn.write(password+"\n")
#tn.write("terminal length 0"+"\n")
tn.read_until(">")
tn.write("en"+"\n")
tn.read_until("Password:")
tn.write(password+"\n")
tn.read_until("#")
tn.write("dir"+"\n")
tn.write("copy nvram startup-config tftp 10.1.1.6 CMTSs/today/wmtn4.cfg18051609" +"\n")
tn.write("exit"+"\n")
print tn.read_until("#\r\n",3)
tn.close()

#print tn.read_all()
#output=tn.read_all()

#filename = "%s_%.2i-%.2i-%i_%.2i-%.2i-%.2i" % (filename_prefix,now.day,now.month,now.year,now.hour,now.minute,now.second)

#fp=open(filename,"w")
#fp.write(output)
#fp.close()
