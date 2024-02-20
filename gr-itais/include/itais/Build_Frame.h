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

#ifndef INCLUDED_ITAIS_BUILD_FRAME_H
#define INCLUDED_ITAIS_BUILD_FRAME_H

#include <itais/api.h>
#include <gnuradio/tagged_stream_block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API Build_Frame : virtual public gr::tagged_stream_block
{
public:
    typedef boost::shared_ptr<Build_Frame> sptr;

    /*!
     * \brief Builds an AIS Frame of 256 bytes.
     *
     * This module does, in order:
     * 1. Payload (NMEA sentence) encoding (6 bits per ASCII)
     * 2. CRC generation [16]
     * 3. Reverse bit order (payload + crc)
     * 4. Stuffing (payload + crc)
     * 5. Headers (Preamble [24], Start [8], Trailer [8], 0x00 Padding)
     * 6. NRZI conversion (enabled by default)
     *
     */
    static sptr
    make(bool repeat, bool enable_NRZI, const std::string& lengthtagname = "packet_len");
};
  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_BUILD_FRAME_H */

