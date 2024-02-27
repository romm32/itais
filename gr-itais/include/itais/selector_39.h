/* -*- c++ -*- */
/*
 * Copyright 2024 gr-itais author.
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

#ifndef INCLUDED_ITAIS_SELECTOR_39_H
#define INCLUDED_ITAIS_SELECTOR_39_H

#include <itais/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace itais {

    /*!
     * \brief <+description of block+>
     * \ingroup itais
     *
     */
    class ITAIS_API selector_39 : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<selector_39> sptr;

      static sptr
    make(size_t itemsize, unsigned int input_index, unsigned int output_index);

    // When enabled is set to false, no output samples are produced
    // Otherwise samples are copied to the selected output port
    virtual void set_enabled(bool enable) = 0;
    virtual bool enabled() const = 0;

    virtual void set_input_index(unsigned int input_index) = 0;
    virtual int input_index() const = 0;

    virtual void set_output_index(unsigned int output_index) = 0;
    virtual int output_index() const = 0;
    };

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_SELECTOR_39_H */
