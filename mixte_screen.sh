#!/bin/bash

if [[ $5 == "" ]]; then
    echo "Usage: $0 $1 name command";
    exit 1;
fi

cd /home/tbn/Desktop/INT_Network_2022/
#cd /home/thierno/INT_Network_2022

name=mixte_$2_$3_$4_$5_$6_$7
#pathruns="/home/tbn/Desktop/INT_Network_2022/runs/hybrid/$1/$2_$4_$5/$6_$7";
pathruns="runs/hybrid/$1/$2_$4_$5/$6_$7";
command=${pathruns}/${name}.sh
#name=$2 
#command=$3
#path="/home/tbn/Desktop/INT_Network_2022/logs/hybrid/$1/$2_$4_$5/$6_$7";
path="logs/hybrid/$1/$2_$4_$5/$6_$7";
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
#./mixte_screen.sh Lattice/16_2022_2_8 16 16 8 4 90 17
#./screen.sh Lattice/16_2022_2_8 mixte_16_16_8_2_90_17 /home/tbn/Desktop/INT_Network_2022/runs/Lattice/16_2022_2_8/model_16_16_8_2.sh

#./screen.sh Lattice/16_2022_2_8 16 16 8 4 /home/tbn/Desktop/INT_Network_2022/runs/Lattice/16_2022_2_8/model_16_16_8_4.sh
