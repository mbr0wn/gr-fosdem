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


class OFDMChatApp(gr.top_block):
    def __init__(self, min_tx_len):
        gr.top_block.__init__(self, "OFDMChatApp")
        # Variables
        self.samp_rate = samp_rate = 1e6
        self.len_tag_key = len_tag_key = "packet_len"
        self.gain = gain = 60
        self.fft_len = fft_len = 128
        self.min_tx_len = min_tx_len
        self.pdu_port = pmt.intern("pdus")
        # Blocks
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format="fc32",
                channels=range(1),
            ),
        )
        self.uhd_usrp_sink_0.set_subdev_spec("A:A", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(400e6, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
            interpolation=2,
            decimation=1,
            taps=None,
            fractional_bw=None,
        )
        self.fosdem_burst_marker_0 = fosdem.burst_marker(gr.sizeof_gr_complex, len_tag_key, 0)
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  packet_length_tag_key=len_tag_key,
        	  bps_header=1,
        	  bps_payload=2,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=True
        	 )
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, len_tag_key, 2)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.05, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.fosdem_burst_marker_0, 0))
        self.connect((self.fosdem_burst_marker_0, 0), (self.uhd_usrp_sink_0, 0))


    def post(self, message_str):
        """ Post a message for tx """
        vect = pmt.make_u8vector(max(len(message_str), self.min_tx_len), ord(' '))
        for i in range(len(message_str)):
            pmt.u8vector_set(vect, i, ord(message_str[i]))
        meta = pmt.PMT_NIL
        msg = pmt.cons(meta, vect)
        self.blocks_pdu_to_tagged_stream_0.to_basic_block()._post(self.pdu_port, msg)


if __name__ == "__main__":
    ChatApp = OFDMChatApp(min_tx_len=50)
    ChatApp.start()
    time.sleep(1)
    while True:
        try:
            msg_str = raw_input('> ')
            if msg_str == '/quit' or msg_str == '/q':
                break
        except EOFError:
            break
        ChatApp.post(msg_str)
        ChatApp.post('')
    ChatApp.stop()
    ChatApp.wait()

