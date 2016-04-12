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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import fosdem_swig as fosdem

class qa_burst_marker (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):

        packet_len = 96;
        pad_zeros = 4;
        len_tag_key = 'packet_len'
        src = blocks.vector_source_f(range(packet_len), False)
        sink = blocks.vector_sink_f()
        self.tb.connect(
            src,
            blocks.stream_to_tagged_stream(gr.sizeof_float, 1, packet_len, len_tag_key),
            fosdem.burst_marker(gr.sizeof_float, len_tag_key, pad_zeros),
            sink,
        )
        self.tb.run ()
        self.assertFloatTuplesAlmostEqual(sink.data(), range(packet_len) + [0.0,] * pad_zeros)
        tags = [gr.tag_to_python(x) for x in sink.tags()]
        tags = sorted([(x.offset, x.key, x.value) for x in tags])
        tags_expected = [
            (0,                            len_tag_key, packet_len + pad_zeros), # Hard coded time value :( Is n_zeros/sampling_rate
            (0,                           'tx_sob',  True),
            (packet_len + pad_zeros - 1,  'tx_eob',  True),
        ]
        self.assertEqual(tags, tags_expected)
        print tags


if __name__ == '__main__':
    gr_unittest.run(qa_burst_marker, "qa_burst_marker.xml")
