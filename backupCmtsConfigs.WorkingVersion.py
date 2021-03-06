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


## Variables
Log = "/root/backup.Log"
tftpServer = "10.1.1.5"
now = datetime.date.today()
currDate = str(now)
currDate = currDate.replace('-', '')  ## Result is yymmdd
#print "Date is " + str(currDate)
cmtsList = "/root/cmtsName.txt"
tftpboot = "/var/lib/tftpboot/"

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
	if cmtsType == 'casa':
		saveCommand = "copy nvram startup-config tftp " + tftpServer + saveName
		commands = ["root","casa","en","casa",saveCommand,""]
	if cmtsType == 'ubr':
        	commands = ["1234","en","1234",saveCommand,"",""]

	## Telnet variables
	HOST = cmtsName
	PORT = 23
	TIMEOUT = 3
	tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
	tn.write("\r\n\r\n")
	for cmd in commands:
		tn.write(cmd+"\r\n")
	print tn.read_until("#\r\n",3)
	tn.close()


def verifySaved(configName):
	## Verify has the config been saved
	status = os.stat(configName).st_size == 0
	#if status <> True:
	if status <> True:
		logString = configName, "is not an empty file"
		logWrite(logString)
	else:
		logString =  configName, "is an empty file"
		logWrite(logString)
		### SEND A TRAP
		subprocess.call(['bash','/root/backupTrap.sh',configName])

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
	saveName = cmtsName  + ".cfg" + currDate			## EG. labrouter.cfg20180509
	configName = tftpboot + cmtsName + ".cfg" + currDate		## EG. /var/lib/tftpboot/labrouter.cfg20180509
	# print "ConfigName", configName
	configFile = open(configName,'w')				## EG. labrouter.cfg20180509
	#configFile.write(comment)					
	configFile.close()
	os.chmod(configName, 0o777)					## chmod to 777
	## Calling saveConfig function
	logString = "Saving ", configName
	logWrite(logString)
	saveConfig(cmtsName,cmtsType,saveName)				## Call function saveConfig and pass variables cmtsName,cmtsType,saveName
	logString = "Verifying ",configName
	logWrite(logString)
	verifySaved(configName)						## Check that the saved file isn't empty
  		
logWrite("END CMTS Backup Process")
