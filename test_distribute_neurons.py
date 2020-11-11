# Example script to distribute neurons across cpu cores to explore multiple parameters or conditions.
# This script is for simulations that do not require neurons to communicate across processes.
from mpi4py import MPI
comm = MPI.COMM_WORLD

from neuron import h
h.load_file('stdrun.hoc')

# Get node ID
rank = comm.Get_rank()

# Get total number of processes
nhost = comm.Get_size()

print('%i out of %i' % (rank, nhost))

# Single compartment HH model of neuron
import Cell

# NetStim to generate random input
import SpikingInput

import numpy as np
import h5py
import datetime
import time as cookie
date = str(datetime.date.today())

# Define parameters to be investigated
# Factors will be multipled to the 
# Na and K channel conductances
n_factor = 5
factors = np.linspace(0.5, 1.5, n_factor)
f1, f2 = np.meshgrid(factors, factors)
f1 = f1.flatten()
f2 = f2.flatten()

# Create postsynaptic cells - single compartment hh neuron
# Round-robin distribution of neurons
post_cells = []
for ii in range(rank, len(f1), nhost):
    ID = ii
    post_cells.append(Cell.Create(ID))
    for seg in post_cells[-1].sec:
        seg.hh.gnabar *= f1[ii]
        seg.hh.gkbar *= f2[ii]

# Create presynaptic cells - spike generators
# Each process needs to create all inputs because
# there is not cross-process communication
n_pre = 20
freq = 5 # units: Hz
tstop = 10000 # units: ms
pre_cells = []
ID = len(f1)
for ii in range(n_pre):
    ID = ii + len(f1)
    pre_cells.append(SpikingInput.Create(ID, freq, tstop))

# Connect presynaptic to postsynaptic
weight_pre = 0.05
net_cons = []
for post in post_cells:
    for pre in pre_cells:
        nc = h.NetCon(pre.stim, post.syn_list[0])
        nc.weight[0] = weight_pre
        nc.delay = 1
        net_cons.append(nc)

# Instrument cells to record spike times
tvec = h.Vector()
idvec = h.Vector()
for post in post_cells:
    post.spike_detector.record(tvec, idvec, post.ID)

for pre in pre_cells:
    pre.spike_detector.record(tvec, idvec, post.ID)

# Record voltage
v = {}
for post in post_cells:
    v[post.ID] = h.Vector()
    v[post.ID].record(post.sec(0.5)._ref_v, sec=post.sec)

if rank == 0:
    t = h.Vector()
    t.record(h._ref_t)

# Initialize simulation
v_init = -65
dt = 0.025

h.finitialize(v_init)
h.dt = dt
h.fcurrent()
h.frecord_init()

# Run simulation
start = cookie.time()
h.continuerun(tstop)
stop = cookie.time()

if rank == 0:
    print('Took %.3f seconds' % (stop-start))

tvec = np.array(tvec)
idvec = np.array(idvec)

# Initialize data file
if rank == 0:
    with h5py.File('data_distribute_neurons_%s.h5' % date, 'w') as dset:
        dset.create_group('Spike Times')
        dset.create_group('Voltages')
        dset['t'] = np.array(t)
        dset['Sodium Factor'] = f1
        dset['Potassium Factor'] = f2
        dset['IDs'] = np.arange(len(f1))
        
        # All processes created the same inputs so only one
        # process should save them out.
        for pre in pre_cells:
            spiketimes = tvec[idvec == pre.ID]
            dset['Spike Times'][str(pre.ID)] = spiketimes

# Wait for data file to be created before continuing
comm.barrier()

# Save data
# Have individual processes write their data to file.
# Exception handling for cases when the file is accessed
# simultaneously which can lead to an OSError.
flag = 1
while flag:
    try:
        with h5py.File('data_distribute_neurons_%s.h5' % date, 'a') as dset:
            for post in post_cells:
                spiketimes = tvec[idvec == post.ID]
                dset['Spike Times'][str(post.ID)] = spiketimes
                dset['Voltages'][str(post.ID)] = np.array(v[post.ID])
        
        flag = 0
    
    except OSError:
        pass

exit()
