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


#ifndef INCLUDED_FOSDEM_BURST_MARKER_H
#define INCLUDED_FOSDEM_BURST_MARKER_H

#include <fosdem/api.h>
#include <gnuradio/tagged_stream_block.h>

namespace gr {
  namespace fosdem {

    /*!
     * \brief <+description of block+>
     * \ingroup fosdem
     *
     */
    class FOSDEM_API burst_marker : virtual public gr::tagged_stream_block
    {
     public:
      typedef boost::shared_ptr<burst_marker> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of fosdem::burst_marker.
       *
       * To avoid accidental use of raw pointers, fosdem::burst_marker's
       * constructor is in a private implementation
       * class. fosdem::burst_marker::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t itemsize, const std::string &len_tag_key, int pad_zeros=0);
    };

  } // namespace fosdem
} // namespace gr

#endif /* INCLUDED_FOSDEM_BURST_MARKER_H */

