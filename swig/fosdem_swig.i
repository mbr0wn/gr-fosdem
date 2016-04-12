/* -*- c++ -*- */

#define FOSDEM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "fosdem_swig_doc.i"

%{
#include "fosdem/burst_marker.h"
%}


%include "fosdem/burst_marker.h"
GR_SWIG_BLOCK_MAGIC2(fosdem, burst_marker);
