/* -*- c++ -*- */
/*
 * Copyright 2024 bistromath.
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

#ifndef INCLUDED_ITAIS_FREQEST_H
#define INCLUDED_ITAIS_FREQEST_H

#include <itais/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API freqest : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<freqest> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of ais::freqest.
       *
       * To avoid accidental use of raw pointers, ais::freqest's
       * constructor is in a private implementation
       * class. ais::freqest::make is the public interface for
       * creating new instances.
       */
      static sptr make(float sample_rate, int data_rate, int fftlen);
    };


  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_FREQEST_H */

