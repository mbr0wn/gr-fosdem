#!/usr/bin/env python

import pmt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
import fosdem
import pmt
import sys
import time
import osmosdr

class OFDMChatAppRx(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "OFDMChatAppRx")

        ##################################################
        # Variables
        ##################################################
        self.tune_offset = tune_offset = 500e3
        self.samp_rate = samp_rate = 500000
        self.len_tag_key = len_tag_key = "packet_len"
        self.fft_len = fft_len = 128
        self.decimation = decimation = 4

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate*decimation)
        self.osmosdr_source_0.set_center_freq(400e6-tune_offset, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(0, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(
                decimation,
                (filter.firdes.low_pass(1.0, samp_rate*decimation, 300e3, 100e3)),
                tune_offset,
                samp_rate*decimation
        )
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  frame_length_tag_key='frame_'+"rx_len",
        	  packet_length_tag_key="rx_len",
        	  bps_header=1,
        	  bps_payload=2,
        	  debug_log=False,
        	  scramble_bits=True
         )
        self.tagged_stream_to_pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, 'rx_len')
        self.pdu_receiver = fosdem.pdu_receiver()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.digital_ofdm_rx_0, 0), self.tagged_stream_to_pdu)
        self.msg_connect(self.tagged_stream_to_pdu, "pdus", self.pdu_receiver, "pdus")

if __name__ == "__main__":
    ChatAppRx = OFDMChatAppRx()
    ChatAppRx.start()
    time.sleep(1)
    while True:
        try:
            msg_str = raw_input('> ')
            if msg_str == '/quit' or msg_str == '/q':
                break
        except EOFError:
            break
    ChatAppRx.stop()
    ChatAppRx.wait()

