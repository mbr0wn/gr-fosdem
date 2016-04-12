#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Strobe
# Generated: Sat Feb 22 16:51:17 2014
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt

class strobe(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Strobe")

        ##################################################
        # Blocks
        ##################################################
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.cons( pmt.PMT_NIL, pmt.make_u8vector(64,0) ), 750)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_copy_0 = blocks.copy(gr.sizeof_char*1)
        self.blocks_copy_0.set_enabled(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_copy_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_copy_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.blocks_message_strobe_0, "strobe", self.blocks_message_debug_0, "print")
        self.msg_connect(self.blocks_message_strobe_0_0, "strobe", self.blocks_pdu_to_tagged_stream_0, "pdus")
        self.msg_connect(self.blocks_tagged_stream_to_pdu_0, "pdus", self.blocks_message_debug_0, "print_pdu")

# QT sink close method reimplementation

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = strobe()
    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

