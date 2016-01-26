#!/bin/bash
set -x
DATE=`date +%Y-%m-%d:%H:%M:%S`
echo $DATE
echo "Begin..."
source /root/.bashrc
pushd /root/jingmei/
python collector.py
sleep 10
python retry_articles.py
sleep 10
perl relevancy.pl
DATE=`date +%Y-%m-%d:%H:%M:%S`
echo $DATE
echo "Done!"
exit
