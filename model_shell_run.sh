#!/bin/bash


cd /home/tbn/Desktop/INT_Network_2022
#cd /home/thierno/INT_Network_2022
mkdir -p runs/basic/$1/$2_$4_$5
mkdir -p solutions/basic/$1/$2_$4_$5

arr=($3)

for i in "${!arr[@]}"; do
./screen_model_run.sh $1 $2 ${arr[i]} $4 $5 $6 $7 > runs/basic/$1/$2_$4_$5/model_$2_${arr[i]}_$4_$5.sh
chmod +x runs/basic/$1/$2_$4_$5/model_$2_${arr[i]}_$4_$5.sh

./model_screen.sh $1 $2 ${arr[i]} $4 $5
done
#./screen_model_run.sh $1 $2 $3 $4 $5 $6 $7 > runs/$1/$2_$4_$5/model_$2_$3_$4_$5.sh
#chmod +x runs/$1/$2_$4_$5/model_$2_$3_$4_$5.sh

#./screen.sh $1 $2 $3 $4 $5


#how to run 
#./screen_model_run.sh Lattice/16_2022_2_8 16 16 8 2 2 8 > runs/Lattice/16_2022_2_8/16_8_2/model_16_16_8_2.sh
#./model_screen.sh Lattice/16_2022_2_8 16 16 8 4
#./model_shell_run.sh Lattice/16_2022_2_8 16 "16 32 64 128" 8 2 2 8




#List="abcd 1234 jvm something"
#arr=($List)
#echo ${arr[0]}
#for i in ${arr[*]}; do
#echo $i
#done

#List="abcd 1234 jvm something"
#arr=($List)
#for i in "${!arr[@]}"; do
#  printf '${arr[%s]}=%s\n' "$i" "${arr[i]}"
#done


#List="abcd 1234 jvm something"
#arr=($List)
#for i in "${!arr[@]}"; do
#  echo "$i" "${arr[i]}"
#done


#echo "${!arr[@]}"



