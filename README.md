The steps are explained and relevant commands are shown below each step.
Obtain the latest source files from Github. The repo name is backupCmtsConfig. Procedure to install from Github is 
https://docs.google.com/document/d/18qzqfG9P1Xvcekl66uED4XuH9c6iUKmU3s9CoOxRRrg

1.  Cd to /opt. This is where the source files will be saved to.     
    cd /opt
    
2.  Clone the Github files from the repo backupCmtsConfig to /opt/ on your server. It will create a directory called backupCmtsConfigs
    git clone https://github.com/pnetDev/backupCmtsConfigs.git

3.  Edit /opt/backupCmtsConfigs/cmtsName.txt to refer to the CMTS hostnames you need to backup.
    vim /opt/backupCmtsConfigs/cmtsName.txt

4.  Change the variable tftpboot in the Python script to refer to the path where your config files are to be saved to and change variable tftpServer to the ip address of your server.
    vim /opt/backupCmtsConfigs/backupCmtsConfigs.py

5.  Run the script backupCmtsConfigs.py and events will be logged to /var/log/backup.Log
    /opt/backupScripts/backupCmtsConfigs.py
