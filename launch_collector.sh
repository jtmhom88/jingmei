#!/bin/bash
set -x
DATE=`date +%Y-%m-%d:%H:%M:%S`
echo $DATE
echo "Begin..."
# Check to see if collector job is running
SERVICE='run_collector_job.sh'
 
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
  echo "$SERVICE service running, exiting..."
  exit
else
  echo "$SERVICE is not running"
  echo "start job..."
  pushd /root/jingmei/
  bash -x run_collector_job.sh > /tmp/collector.job.log  2>&1
fi

DATE=`date +%Y-%m-%d:%H:%M:%S`
echo $DATE
echo "Done!"
exit
