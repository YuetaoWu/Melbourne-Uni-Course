#!/usr/bin/env python
#
# Copyright 2012,2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

"""
BER simulation for QPSK signals, compare to theoretical values.
Change the N_BITS value to simulate more bits per Eb/N0 value,
thus allowing to check for lower BER values.

Lower values will work faster, higher values will use a lot of RAM.
Also, this app isn't highly optimized--the flow graph is completely
reinstantiated for every Eb/N0 value.
Of course, expect the maximum value for BER to be one order of
magnitude below what you chose for N_BITS.
"""


import numpy as np
from gnuradio import gr, digital
from gnuradio import analog
from gnuradio import blocks
import sys

try:
    from scipy.special import erfc
except ImportError:
    print "Error: could not import scipy (http://www.scipy.org/)"
    sys.exit(1)

try:
    import pylab
except ImportError:
    print "Error: could not import pylab (http://matplotlib.sourceforge.net/)"
    sys.exit(1)

# Useful constants
N_BITS = 1e7
RAND_SEED = 25
PI = np.pi

### Step 2 ###
def berawgn(M, EbN0):
    """ Calculates the theoretical bit error rate in AWGN (for MPSK and given Eb/N0) """
    EbN0 = 1.0*10**(0.1*float(EbN0))
    if M == 2:
        P_b = 0.5*erfc(np.sqrt(EbN0))
    elif M == 4:
        P_e = erfc(np.sqrt(EbN0))-np.square(0.5*erfc(EbN0))
        P_b = P_e/np.log2(M) 

    else:
        P_e = erfc(np.sqrt(np.log2(M)*np.square(np.sin(PI/M))*EbN0))
        P_b = P_e/(np.log2(M))

    return P_b

class BitErrors(gr.hier_block2):
    """ Two inputs: true and received bits. We compare them and
    add up the number of incorrect bits. Because integrate_ff()
    can only add up a certain number of values, the output is
    not a scalar, but a sequence of values, the sum of which is
    the BER. """
    def __init__(self, bits_per_byte):
        gr.hier_block2.__init__(self, "BitErrors",
                gr.io_signature(2, 2, gr.sizeof_char),
                gr.io_signature(1, 1, gr.sizeof_int))
        # Bit comparison
        comp = blocks.xor_bb()
        intdump_decim = 100000
        if N_BITS < intdump_decim:
            intdump_decim = int(N_BITS)
        self.connect(self,
                     comp,
                     blocks.unpack_k_bits_bb(bits_per_byte),
                     blocks.uchar_to_float(),
                     blocks.integrate_ff(intdump_decim),
                     blocks.multiply_const_ff(1.0/N_BITS),
                     self)
        self.connect((self, 1), (comp, 1))


class BERAWGNSimu(gr.top_block):
    " This contains the simulation flow graph "
    def EbN0_to_noise_voltage(self, EbN0):
        """ Converts Eb/N0 to a complex noise voltage (assuming unit symbol power) """
        return 1.0 / np.sqrt(self.const.bits_per_symbol() * 10**(float(EbN0)/10))

    def __init__(self, M, EbN0):
        gr.top_block.__init__(self)
        self.const = digital.psk_constellation(m=M)
        # Source is N_BITS bits, non-repeated
        data = map(int, np.random.randint(0, self.const.arity(), int(N_BITS/self.const.bits_per_symbol())))
        src   = blocks.vector_source_b(data, False)
        mod   = digital.chunks_to_symbols_bc((self.const.points()), 1)
        add   = blocks.add_vcc()
        noise = analog.noise_source_c(analog.GR_GAUSSIAN,
                                      self.EbN0_to_noise_voltage(EbN0),
                                      RAND_SEED)
        demod = digital.constellation_decoder_cb(self.const.base())
        ber   = BitErrors(self.const.bits_per_symbol())
        self.sink  = blocks.vector_sink_f()
        
        ### Step 3 ###
        self.connect(src,mod,(add,0),demod,(ber,0),self.sink)
        self.connect(noise,(add,1))
        self.connect(src,(ber,1))
        
        ### END ###
        

def simulate_ber(M, EbN0):
    """ All the work's done here: create flow graph, run, read out BER """
    print "%dPSK Modulation @ Eb/N0 = %d dB" % (M, EbN0)
    fg = BERAWGNSimu(M, EbN0)
    fg.run()
    return np.sum(fg.sink.data())

if __name__ == "__main__":
    EbN0_min = -4
    EbN0_max = 24
    EbN0_range = np.arange(EbN0_min, EbN0_max+1, 2)
    print "Calculating..."

    ber_theory = []
    
    ### Step 4 ###
    ### START CODE HERE ### (~5 line)
    for i in range(5):
        ber_theory.append([berawgn(1<<(i+1),snr) for snr in EbN0_range])
   
    ### END ###
    
    print "Simulating..."
    
    
    ### Step 5 ###
    ### START CODE HERE ### (~5 line)
    for i in range(5):
        ber_simu.append([simulate_ber(1<<(i+1),snr) for snr in EbN0_range])
    ### END ###
    
    f = pylab.figure()
    s = f.add_subplot(1,1,1)
    s.semilogy(EbN0_range, ber_theory[0], 'b-.', label="BPSK Theoretical")
    s.semilogy(EbN0_range, ber_theory[1], 'r-.', label="QPSK LB")
    s.semilogy(EbN0_range, ber_theory[2], 'c-.', label="8PSK LB")
    s.semilogy(EbN0_range, ber_theory[3], 'm-.', label="16PSK LB")
    s.semilogy(EbN0_range, ber_theory[4], 'k-.', label="32PSK LB")
    
    s.semilogy(EbN0_range, ber_simu[0], 'b-o', label="BPSK Simulation")
    s.semilogy(EbN0_range, ber_simu[1], 'r-o', label="QPSK Simulation")
    s.semilogy(EbN0_range, ber_simu[2], 'c-o', label="8PSK Simulation")
    s.semilogy(EbN0_range, ber_simu[3], 'm-o', label="16PSK Simulation")
    s.semilogy(EbN0_range, ber_simu[4], 'k-o', label="32PSK Simulation")
    
    s.set_title('BER Simulation')
    s.set_xlabel('Eb/N0 (dB)')
    s.set_ylabel('BER')
    s.set_ylim([10e-6, 1])
    s.legend(loc='lower left')
    s.grid()
    pylab.show()

