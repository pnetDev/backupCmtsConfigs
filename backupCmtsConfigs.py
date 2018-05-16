#!/usr/bin/python

## CM 180509. This script will backup the start-up config of a CMTS.
## The script will read the CMTS name and type from cmtsName.txt and do the following:
## An empty config file is written to ~tftpboot with a time stamp suffix E.G.
## 	Mish1.cfg180509
## The file must have world write permission.
## The Python script runs the appropriate function for the CMTS type and telnets to the CMTS
## The startup-configuration of the CMTS is saved to the backup server using tftp
## The Python script logs out of CMTS
## The Python script checks that the configuration was saved successfully and will send an snmp trap if it finds a problem.
## The Python script reads the next CMTS from cmtsList.txt

## Required modules
import telnetlib,datetime,os,subprocess
from time import gmtime, strftime

## Variables
Log = "/var/log/cmtsBackup.Log"
tftpServer = "10.1.1.6"
## New code to show date as YYMMDDHH
now = strftime("%y%m%d%H")		# New code to show date as YYMMDDHH
#now = datetime.date.today()
currDate = str(now)
#currDate = currDate.replace('-', '')  ## Result is yymmdd
#print "Date is " + str(currDate)
cmtsList = "/opt/backupCmtsConfigs/cmtsName.txt"
tftpboot = "/pnetBackup/tftpboot/CMTSs/today/"
path = "CMTSs/today"
#=============================================================================================================================#

## Functions

def logWrite(logText):
	now =  datetime.datetime.now()
	logDate = str(now)
        logText = str(logText)
        file = open(Log,'a')
        file.write(logDate + " backupCmtsConfigs.py \t")
	file.write(logText)
	file.write('\n')


def saveConfig(cmtsName,cmtsType,saveName):
	#print configName
	saveCommand = "copy start tftp://" + tftpServer + "/" + saveName ## For arris, cisco, bsr
	#commands = 0 ## We have to assign a value to the variable
	print ""
	print "Called saveConfig ",cmtsName,cmtsType
        if cmtsType == 'arris':
		 commands = ["hsds","hsds","en","hsds",saveCommand,"",""]
	if cmtsType == 'bsr':
		commands =  ["hsds","en","hsds",saveCommand,"",""]
	#if cmtsType == 'casa':
		#backupCasaConfig()
		#saveCommand = "copy nvram startup-config tftp " + " " + tftpServer + " " + saveName
		#commands = ["root","casa","en","casa",saveCommand,""]
		#commands = ["root","casa","en","casa"]
	if cmtsType == 'ubr':
        	commands = ["1234","en","1234",saveCommand,"",""]

	## Telnet variables
	HOST = cmtsName
	PORT = 23
	TIMEOUT = 3
	try:
		tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
	except:
		print "Unable to contact", HOST
		logString = HOST, "Unable to contact"
		logWrite(logString)
		return				# Exit the function and return to main
	
	tn.write("\r\n\r\n")
	logString = HOST, "Connect successful. Saving config."
	logWrite(logString)
	for cmd in commands:
		tn.write(cmd+"\r\n")
	print tn.read_until("#\r\n",3)
	tn.close()
	
def saveConfigCasa(cmtsName,cmtsType,saveName):
	host = cmtsName
	username = "root"
	password = "casa"
	saveCommand = "copy nvram startup-config tftp " + " " + tftpServer + " " + saveName
	print saveCommand
	tn = telnetlib.Telnet(host)
	tn.read_until("login:")
	tn.write(username+"\n")
	tn.read_until("Password:")
	tn.write(password+"\n")
	tn.read_until(">")
	tn.write("en"+"\n")
	tn.read_until("Password:")
	tn.write(password+"\n")
	tn.read_until("#")
	tn.write(saveCommand +"\n")
	tn.write("exit"+"\n")
	print tn.read_until("#\r\n",3)
	tn.close()
	

def verifySaved(configName):
	## Verify has the config been saved
	status = os.stat(configName).st_size == 0
	#if status <> True:
	if status <> True:
		logString = configName, "BACKUP: SUCCESSFUL"
		logWrite(logString)
	else:
		logString =  configName, "BACKUP: FAILED - file is empty"
		logWrite(logString)
		### SEND A TRAP
		subprocess.call(['bash','/opt/backupCmtsConfigs/backupTrap.sh',configName])

#=================================================================================================================================================#

## Main

logWrite("START CMTS Backup Process")
## Open cmtsList and read CMTS name and type
for cmts in open(cmtsList,'r'):
	cmtsName = cmts.split(",")[0]
	cmtsType = cmts.split(",")[1]
	cmtsType = cmtsType.replace("\n","")				## Need to remove \n from the string for if to work
	logString = "Processing ", cmtsName, cmtsType
	logWrite(logString)
	## Create the empty file the startup-config will be saved to
	saveName = path + "/" + cmtsName  + ".cfg" + currDate			## EG. labrouter.cfg20180509
	configName = tftpboot + cmtsName + ".cfg" + currDate		## EG. /var/lib/tftpboot/labrouter.cfg20180509
	# print "ConfigName", configName
	configFile = open(configName,'w')				## EG. labrouter.cfg20180509
	#configFile.write(comment)					
	configFile.close()
	os.chmod(configName, 0o777)					## chmod to 777
	## Calling saveConfig function
	logString = "Connecting to ", cmtsName
	logWrite(logString)
	## The casa needs different syntax so we need to check here if the type is casa
	if cmtsType == "casa":
		print "Casa detected calling saveConfigCasa"
		saveConfigCasa(cmtsName,cmtsType,saveName)
	if cmtsType <> "casa":
		saveConfig(cmtsName,cmtsType,saveName)				## Call function saveConfig and pass variables cmtsName,cmtsType,saveName
	logString = "Verifying ",configName
	logWrite(logString)
	verifySaved(configName)						## Check that the saved file isn't empty
  	
## This code is to scp the saved configs to 10.1.1.223
subprocess.call(['bash','/opt/backupCmtsConfigs/syncConfigWith223.sh',currDate])
	
logWrite("END CMTS Backup Process")
