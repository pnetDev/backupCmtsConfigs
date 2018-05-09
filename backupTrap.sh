#!/bin/bash
trapserver=10.1.1.7
cmts=$1
echo "A trap is sent with text $cmts"
snmptrap -v2c -c public $trapserver 0 0.1 1 s "CMTS BACKUP ERROR" 2 s "$cmts is an empty file";
