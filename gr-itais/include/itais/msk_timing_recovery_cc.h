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

#ifndef INCLUDED_ITAIS_MSK_TIMING_RECOVERY_CC_H
#define INCLUDED_ITAIS_MSK_TIMING_RECOVERY_CC_H

#include <itais/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API msk_timing_recovery_cc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<msk_timing_recovery_cc> sptr;

      /*!
       * \brief Make an MSK timing recovery block.
       *
       * \param sps: Samples per symbol
       * \param gain: Loop gain of timing error filter (try 0.05)
       * \param limit: Relative limit of timing error (try 0.1 for 10% error max)
       * \param osps: Output samples per symbol
       *
       */
      static sptr make(float sps, float gain, float limit, int osps);

      virtual void set_gain(float gain)=0;
      virtual float get_gain(void)=0;

      virtual void set_limit(float limit)=0;
      virtual float get_limit(void)=0;

      virtual void set_sps(float sps)=0;
      virtual float get_sps(void)=0;
    };

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_MSK_TIMING_RECOVERY_CC_H */

