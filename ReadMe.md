# Instances

##Instances are in the folder data/instance_path. But to generate the run file dont write data before the path.

##To generate data use 
python3 GN/int_generate_lattice.py data/instances N D F min_size max_size 
python3 GN/int_generate_lattice.py ./data/Lattice/16_2022_2_8 4 16 16 2 8

1) python3 GN/int_generate_barabasi.py data/instances  D ETA F min_size max_size 
1) python3 GN/int_generate_barabasi.py ./data/Barabasi/16_2_2022_2_8 16 2 16 2 8


## To run the shell use the following command
- for the basic model use :
./model_shell_run instance_path D F=[16 32 64 128] V M min_size max_size
./model_shell_run.sh Lattice/16_2022_2_8 16 "16 32 64 128" 8 2 2 8

- for the hybrid model use : 
#./mixte_shell_run.sh instance_path D F=[16 32 64 128] V M GF min_size max_size max_route
#./mixte_shell_run.sh Lattice/16_2022_2_8 16 "16 32 64 128" 8 2 90 2 8 12
