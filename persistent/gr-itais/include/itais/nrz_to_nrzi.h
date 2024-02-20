/* -*- c++ -*- */
/*
 * Copyright 2024 trendmicro, bmagistro.
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

#ifndef INCLUDED_ITAIS_NRZ_TO_NRZI_H
#define INCLUDED_ITAIS_NRZ_TO_NRZI_H

#include <itais/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API nrz_to_nrzi : virtual public gr::block
{
public:
    typedef boost::shared_ptr<nrz_to_nrzi> sptr;

    /*!
     * \brief Convert from NRZ to NRZI
     *
     * Convert a BYTE sequence from NRZ to NRZI. Note: This is also implemented in the
     * Build_Frame component.
     *
     */
    static sptr make();
};

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_NRZ_TO_NRZI_H */

