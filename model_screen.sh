#!/bin/bash

if [[ $5 == "" ]]; then
    echo "Usage: $0 $1 name command";
    exit 1;
fi

cd /home/tbn/Desktop/INT_Network_2022/
#cd /home/thierno/INT_Network_2022

name=model_$2_$3_$4_$5
pathruns="runs/basic/$1/$2_$4_$5";
#pathruns="/home/tbn/Desktop/INT_Network_2022/runs/basic/$1/$2_$4_$5";
command=${pathruns}/${name}.sh
#name=$2 
#command=$3
path="logs/basic/$1/$2_$4_$5";
#path="/home/tbn/Desktop/INT_Network_2022/logs/basic/$1/$2_$4_$5";
mkdir -p ${path}
config="logfile ${path}/${name}.log
logfile flush 1
log on
logtstamp after 1
logtstamp string \"[ %t: %Y-%m-%d %c:%s ]\012\"
logtstamp on";
echo "$config" > /tmp/log.conf
screen -c /tmp/log.conf -dmSL "$name" $command
rm /tmp/log.conf


#to run it use 
#./model_screen.sh Lattice/16_2022_2_8 16 16 8 4

