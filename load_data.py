# Script to show how to load data

import h5py
import numpy as np

fname = ''

spiketimes = {}
with h5py.File(fname, 'r') as dset:
    for ID in dset['Spike Times']:
        spiketimes[ID] = dset['Spike Times'][ID][:]
