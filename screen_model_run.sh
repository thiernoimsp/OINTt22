#!/bin/bash
cat <<EoF


cd /home/tbn/Desktop/INT_Network_2022
#cd /home/thierno/INT_Network_2022
##python3.7 int_model_base.py data/16_2021 D F V M min_size max_size
##python3.7 int_model_base.py data/16_2021 16 4 8 2 1 4
python3.7 int_model_base.py data/$1 $2 $3 $4 $5 $6 $7


#to run it use 
#1) ./screen_model_run.sh instance_path D F V M min_size max_size > runs/instance_path/D_V_M/model_D_F_V_M.sh
#1) ./screen_model_run.sh Lattice/16_2022_2_8 16 16 8 2 2 8 > runs/Lattice/16_2022_2_8/16_8_2/model_16_16_8_2.sh

EoF
