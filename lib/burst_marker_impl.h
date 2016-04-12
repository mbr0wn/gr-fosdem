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

#ifndef INCLUDED_FOSDEM_BURST_MARKER_IMPL_H
#define INCLUDED_FOSDEM_BURST_MARKER_IMPL_H

#include <fosdem/burst_marker.h>

namespace gr {
  namespace fosdem {

    class burst_marker_impl : public burst_marker
    {
     private:
       size_t d_itemsize;
       int d_pad_zeros;

     protected:
      int calculate_output_stream_length(const gr_vector_int &ninput_items);

     public:
      burst_marker_impl(size_t itemsize, const std::string &len_tag_key, int pad_zeros);
      ~burst_marker_impl();

      int work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace fosdem
} // namespace gr

#endif /* INCLUDED_FOSDEM_BURST_MARKER_IMPL_H */

