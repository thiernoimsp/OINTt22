#!/bin/bash

#cd /home/thierno/INT_Network_2022
cd /home/tbn/Desktop/INT_Network_2022
mkdir -p runs/hybrid/$1/$2_$4_$5/$6_$9
mkdir -p solutions/hybrid/$1/$2_$4_$5/$6_$9

arr=($3)

for i in "${!arr[@]}"; do
./screen_mixte_run.sh $1 $2 ${arr[i]} $4 $5 $6 $7 $8 $9 > runs/hybrid/$1/$2_$4_$5/$6_$9/mixte_$2_${arr[i]}_$4_$5_$6_$9.sh
chmod +x runs/hybrid/$1/$2_$4_$5/$6_$9/mixte_$2_${arr[i]}_$4_$5_$6_$9.sh

./mixte_screen.sh $1 $2 ${arr[i]} $4 $5 $6 $9
done
#./screen_mixte_run.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 > runs/hybrid/$1/$2_$4_$5/$6_$9/mixte_$2_$3_$4_$5_$6_$9.sh
#chmod +x runs/hybrid/$1/$2_$4_$5/$6_$9/mixte_$2_$3_$4_$5_$6_$9.sh

#./mixte_screen.sh $1 $2 $3 $4 $5 $6 $9

#./mixte_shell_run.sh instance_path D F=[16 32 64 128] V M GF min_size max_size max_route
#./mixte_shell_run.sh Lattice/16_2022_2_8 16 "16 32 64 128" 8 2 90 2 8 12
