#!/bin/bash

#SBATCH -J pure_mpi
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=0:02:00
#SBATCH --account=berger_92
#SBATCH --exclusive
#SBATCH --partition=main
#SBATCH --constraint="xeon-4116"
#SBATCH --job-name=distnrn
#SBATCH --output=o_distribute_neurons.txt
#SBATCH --error=e_distribute_neurons.txt

module purge
module load usc
module load python/3.7.6
module load ncurses/6.1
ulimit -s unlimited

export OMP_NUM_THREADS=1


# Change NEURON_PATH to point to your NEURON installation directory
NEURON_PATH=/project/berger_92/geneyu/Big_Model/USC-CARC-test_paranrn/nrn-7.7

export PYTHONPATH=$PYTHONPATH:$NEURON_PATH/lib/python

mpirun -bind-to core -np 4 python test_distribute_neurons.py
