#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import pmt
from gnuradio import gr

class pdu_receiver(gr.sync_block):
    """
    docstring for block pdu_receiver
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="pdu_receiver",
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(pmt.intern('pdus'))
        self.set_msg_handler(pmt.intern('pdus'), self.print_msg)

    def print_msg(self, msg):
        """ Print the rx'd message. """
        meta = pmt.to_python(pmt.car(msg))
        vect = pmt.cdr(msg)
        msg_str = ''.join([chr(pmt.u8vector_ref(vect, i)) for i in range(pmt.length(vect))]).strip()
        if len(msg_str):
            print 'Incoming message: ', msg_str
        print meta

