/* -*- c++ -*- */

#define ITAIS_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "itais_swig_doc.i"

%{
#include "itais/corr_est_cc.h"
#include "itais/freqest.h"
#include "itais/invert.h"
#include "itais/pdu_to_nmea.h"
#include "itais/msk_timing_recovery_cc.h"
#include "itais/Build_Frame.h"
#include "itais/nrz_to_nrzi.h"
#include "itais/DebugME.h"
%}

%include "itais/corr_est_cc.h"
GR_SWIG_BLOCK_MAGIC2(itais, corr_est_cc);
%include "itais/freqest.h"
GR_SWIG_BLOCK_MAGIC2(itais, freqest);
%include "itais/invert.h"
GR_SWIG_BLOCK_MAGIC2(itais, invert);

%include "itais/pdu_to_nmea.h"
GR_SWIG_BLOCK_MAGIC2(itais, pdu_to_nmea);

%include "itais/msk_timing_recovery_cc.h"
GR_SWIG_BLOCK_MAGIC2(itais, msk_timing_recovery_cc);
%include "itais/Build_Frame.h"
GR_SWIG_BLOCK_MAGIC2(itais, Build_Frame);
%include "itais/nrz_to_nrzi.h"
GR_SWIG_BLOCK_MAGIC2(itais, nrz_to_nrzi);
%include "itais/DebugME.h"
GR_SWIG_BLOCK_MAGIC2(itais, DebugME);
