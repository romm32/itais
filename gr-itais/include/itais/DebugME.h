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

#ifndef INCLUDED_ITAIS_DEBUGME_H
#define INCLUDED_ITAIS_DEBUGME_H

#include <itais/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API DebugME : virtual public gr::block
{
public:
    typedef boost::shared_ptr<DebugME> sptr;

    /*!
     * \brief Print the incoming BYTE sequence as sequence of HEXs
     *
     * Goes through the incoming sequence (const char *in) and prints it in HEXs
     */
    static sptr make(size_t itemsize);
};

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_DEBUGME_H */

