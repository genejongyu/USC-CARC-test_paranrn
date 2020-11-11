# Example script to distribute a neuronal network across multiple cpu-cores and
# run a simulation that allows neurons from different processes to communicate
# with each other.
from neuron import h
h.nrnmpi_init()

pc = h.ParallelContext()
h.load_file('stdrun.hoc')

# Get node ID
rank = int(pc.id())

# Get total number of processes
nhost = int(pc.nhost())

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

# Create postsynaptic cells - single compartment hh neuron
# Round-robin distribution of neurons
n_post = 100
post_cells = []
ID = rank
for ii in range(rank, n_post, nhost):
    post_cells.append(Cell.Create(ID))
    
    # Associate cell ID with node ID
    pc.set_gid2node(ID, rank)
    
    # Associate cell ID with cell's spike NetCon
    pc.cell(ID, post_cells[-1].spike_detector)
    
    ID += nhost

# Create presynaptic cells - spike generators
# Round-robin distribution of inputs
n_pre = 100
freq = 1 # units: Hz
tstop = 10000 # units: ms
pre_cells = []
ID = n_post+rank
for ii in range(rank, n_pre, nhost):
    pre_cells.append(SpikingInput.Create(ID, freq, tstop))
    pc.set_gid2node(ID, rank)
    pc.cell(ID, pre_cells[-1].spike_detector)
    
    ID += nhost

# Connect presynaptic to postsynaptic
weight_pre = 0.05
net_cons = []
for post in post_cells:
    np.random.seed(post.ID)
    rolls = np.random.uniform(0, 1, n_pre)
    
    # Randomly choose 20% of the inputs
    preIDs = np.arange(n_pre)[rolls < 0.2] + n_post
    for preID in preIDs:
        nc = pc.gid_connect(preID, post.syn_list[0])
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

# pc.set_maxstep needs to be called first
# or else events will be delivered
# across different processes.
pc.set_maxstep(10)

h.finitialize(v_init)
h.dt = dt
h.fcurrent()
h.frecord_init()

# Wait for all processes to have completed above code
# before continuing
pc.barrier()

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
    with h5py.File('data_parallel_network_%s.h5' % date, 'w') as dset:
        dset.create_group('Spike Times')
        dset.create_group('Voltages')
        dset['t'] = np.array(t)

pc.barrier()

# Save data
# Have individual processes write their data to file.
# Exception handling for cases when the file is accessed
# simultaneously which can lead to an OSError.
flag = 1
while flag:
    try:
        with h5py.File('data_parallel_network_%s.h5' % date, 'a') as dset:
            for post in post_cells:
                spiketimes = tvec[idvec == post.ID]
                dset['Spike Times'][str(post.ID)] = spiketimes
                dset['Voltages'][str(post.ID)] = np.array(v[post.ID])
            
            for pre in pre_cells:
                spiketimes = tvec[idvec == pre.ID]
                dset['Spike Times'][str(pre.ID)] = spiketimes
        
        flag = 0
    
    except OSError:
        pass

pc.barrier()

pc.done()

exit()
