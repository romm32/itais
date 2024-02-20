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

#ifndef INCLUDED_ITAIS_DEBUGME_IMPL_H
#define INCLUDED_ITAIS_DEBUGME_IMPL_H

#include <itais/DebugME.h>

namespace gr {
  namespace itais {

    class DebugME_impl : public DebugME
{
private:
    size_t d_itemsize;

public:
    DebugME_impl(size_t itemsize);
    ~DebugME_impl() override = default;

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required) override;

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items) override;
};

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_DEBUGME_IMPL_H */

