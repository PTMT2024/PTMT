#!/bin/bash

TARGET=$1
LOGFILE=${TARGET}/memory_usage.log
rm -f ${LOGFILE}

echo "Timestamp,used_mem" > $LOGFILE

while :
do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    USED_MEM=$(free -h | grep Mem | awk '{print $3}')

    echo "$TIMESTAMP, $USED_MEM" >> $LOGFILE
    sleep 5
done