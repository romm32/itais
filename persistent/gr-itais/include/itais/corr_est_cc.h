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

#ifndef INCLUDED_ITAIS_CORR_EST_CC_H
#define INCLUDED_ITAIS_CORR_EST_CC_H

#include <itais/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API corr_est_cc : virtual public gr::sync_block
    {
    public:
      typedef boost::shared_ptr<corr_est_cc> sptr;

      /*!
       * Make a block that correlates against the \p symbols vector
       * and outputs a phase and symbol timing estimate.
       *
       * \param symbols    Set of symbols to correlate against (e.g., a
       *                   sync word).
       * \param sps        Samples per symbol
       * \param mark_delay tag marking delay in samples after the
       *                   corr_start tag
       * \param threshold  Threshold of correlator, relative to a 100%
       *                   correlation (1.0). Default is 0.9.
       */
      static sptr make(const std::vector<gr_complex> &symbols,
                       float sps, unsigned int mark_delay, float threshold=0.9);

      virtual std::vector<gr_complex> symbols() const = 0;
      virtual void set_symbols(const std::vector<gr_complex> &symbols) = 0;
    };


  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_CORR_EST_CC_H */

