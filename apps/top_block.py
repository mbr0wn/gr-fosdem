#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Thu Feb 13 17:04:09 2014
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len")
        self.blocks_tag_debug_1 = blocks.tag_debug(gr.sizeof_char*1, "Pre-CRC", ""); self.blocks_tag_debug_1.set_display(True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, "Post-CRC", ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 100, "packet_len")
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, 100*5)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 255, 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tag_debug_1, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

