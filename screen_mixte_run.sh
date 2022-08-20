#!/bin/bash
cat <<EoF


cd /home/tbn/Desktop/INT_Network_2022
#cd /home/thierno/INT_Network_2022
##python3.7 int_model_mixte.py data/16_2021 D F V M GF min_size max_size max_route
##python3.7 int_model_mixte.py data/16_2021 16 4 8 2 90 1 4 17
python3.7 int_model_mixte.py data/$1 $2 $3 $4 $5 $6 $7 $8 $9


#to run it use 
#1) ./screen_mixte_run.sh instance_path D F V M GF min_size max_size max_route > runs/instance_path/mixte_D_F_V_M_GF_maxroute.sh
#1) ./screen_mixte_run.sh Lattice/64_2022_1_4 64 32 8 2 90 1 4 17 > runs/Lattice/64_2022_1_4/mixte_64_32_8_2_90_17.sh

EoF
