from neuron import h

class Create:
    def __init__(self, ID, frequency, tstop):
        self.ID = ID
        self.frequency = frequency # units: Hz
        
        self.stim = h.NetStim()
        self.stim.interval = 1000/frequency # units: ms
        self.stim.number = int(tstop/1000*frequency*2)
        self.stim.noise = 1.
        self.stim.start = 0
        self.stim.seed(ID)
        
        self.nc_list = []
        
        # Create spike detector
        self.spike_detector = self.connect_pre(None, 0, 0, 0)
    
    # Creates NetCon to detect when an action potential is generated
    def connect_pre(self, target, vthresh, wt, dly):
        nc = h.NetCon(self.stim, target, vthresh, dly, wt)
        return nc
