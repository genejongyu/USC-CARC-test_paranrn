#!/bin/bash

# Specify directory that neuron will be installed
PWD=/project/berger_92/geneyu/Big_Model/USC-CARC-test_paranrn/
DIRNAME=nrn-7.7

DIRINSTALL=$PWD$DIRNAME

# Clear module space
module purge

# Load default environment packages
module load usc

# Load mpi
module load openmpi

# Specify python version
module load python/3.7.6

# Load compiler
module load gcc

# This library is necessary to complete the installation
module load ncurses/6.1

# Unpack installation files
tar -xvf nrn-7.7.tar.gz

# Move into folder
cd nrn-7.7

# Install
./configure --prefix=$DIRINSTALL --without-iv --with-paranrn=dynamic --with-nrnpython=dynamic --with-pyexe=python3 --disable-rx3d
make
make install
