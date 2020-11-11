from neuron import h

class Create:
    def __init__(self, ID):
        self.ID = ID
        self.sec = h.Section()
        self.sec.nseg = 1
        self.sec.Ra = 100
        self.sec.cm = 1
        
        self.sec.insert('hh')
        for seg in self.sec:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003    # Leak conductance in S/cm2
            seg.hh.el = -54.3
        
        self.nc_list = []
        self.syn_list = []
        
        # Create spike detector
        self.spike_detector = self.connect_pre(None, 0, 0, 0)
        
        # Create excitatory synapse
        self.create_syn(0, 1, 30)
    
    # Creates NetCon to detect when an action potential is generated
    def connect_pre(self, target, vthresh, wt, dly):
        nc = h.NetCon(self.sec(0.5)._ref_v, target, vthresh, dly, wt, sec=self.sec)
        return nc
    
    # Create synapse
    def create_syn(self, e, tau1, tau2):
        syn = h.Exp2Syn(self.sec(0.5), sec=self.sec)
        syn.e = e
        syn.tau1 = tau1
        syn.tau2 = tau2
        
        self.syn_list.append(syn)
