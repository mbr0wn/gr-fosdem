/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "burst_marker_impl.h"
#include <iostream>

namespace gr {
  namespace fosdem {

    burst_marker::sptr
    burst_marker::make(size_t itemsize, const std::string &len_tag_key, int pad_zeros)
    {
      return gnuradio::get_initial_sptr
        (new burst_marker_impl(itemsize, len_tag_key, pad_zeros));
    }

    /*
     * The private constructor
     */
    burst_marker_impl::burst_marker_impl(size_t itemsize, const std::string &len_tag_key, int pad_zeros)
      : gr::tagged_stream_block("burst_marker",
              gr::io_signature::make(1, 1, itemsize),
              gr::io_signature::make(1, 1, itemsize), len_tag_key),
      d_itemsize(itemsize),
      d_pad_zeros(pad_zeros)
    {
      std::cout << "[marker] ctor: " << len_tag_key << std::endl;
    }

    /*
     * Our virtual destructor.
     */
    burst_marker_impl::~burst_marker_impl()
    {
    }

    int
    burst_marker_impl::calculate_output_stream_length(const gr_vector_int &ninput_items)
    {
      int noutput_items = ninput_items[0] + d_pad_zeros;
      return noutput_items;
    }

    int
    burst_marker_impl::work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        unsigned char *out = (unsigned char *) output_items[0];

	memcpy((void *) out, (void *) in, d_itemsize * ninput_items[0]);
	memset((void *) (out + d_itemsize * ninput_items[0]), 0x00, d_pad_zeros * d_itemsize);
	add_item_tag(0, nitems_written(0), pmt::string_to_symbol("tx_sob"), pmt::PMT_T);
	add_item_tag(
	    0,
	    nitems_written(0) + ninput_items[0] + d_pad_zeros - 1,
	    pmt::string_to_symbol("tx_eob"),
	    pmt::PMT_T
	);

        return ninput_items[0] + d_pad_zeros;
    }

  } /* namespace fosdem */
} /* namespace gr */

