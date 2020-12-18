#!/bin/bash

# Specify directory that neuron will be installed
PWD=/project/berger_92/geneyu/Big_Model/USC-CARC-test_paranrn/
DIRNAME=lib-7.7

DIRINSTALL=$PWD$DIRNAME

module purge
module load usc
module load python/3.7.6

cd nrn-7.7/src/nrnpython
python3 setup.py install --prefix=$DIRINSTALL
