#!/usr/bin/env python

import numpy
import pmt
from gnuradio import gr

class mac(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self, name="mac", in_sig=None, out_sig=None)
        self.message_port_register_in(pmt.intern('pdus'))
        self.message_port_register_out(pmt.intern('data'))
        self.set_msg_handler(pmt.intern('pdus'), self.receive_pdu_from_phy)

    def receive_pdu_from_phy(self, msg):
        meta = pmt.to_python(pmt.car(msg)) # This is a dictionary!
        vect = pmt.cdr(msg)
        self._evaluate_metadata(meta)
        self._send_pdu_to_higher_layer(meta, vect)

    def send_pdu_to_phy(self, data):
        meta = {'tx_time': self._calculate_next_tx_time()}
        pdu = pmt.cons(meta, data)
        self.message_port_pub('data', pdu)

