#!/bin/bash
currDate=$1
echo "This is the subprocess"
scp /pnetBackup/tftpboot/CMTSs/today/*$currDate root@10.1.1.223://pnetBackup/tftpboot/CMTSs/today

