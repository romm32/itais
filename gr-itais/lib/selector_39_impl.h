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

#ifndef INCLUDED_ITAIS_SELECTOR_39_IMPL_H
#define INCLUDED_ITAIS_SELECTOR_39_IMPL_H

#include <itais/selector_39.h>
#include <gnuradio/thread/thread.h>


namespace gr {
  namespace itais {

    class selector_39_impl : public selector_39
    {
     private:
     const size_t d_itemsize;
     bool d_enabled;
     unsigned int d_input_index, d_output_index;
     unsigned int d_num_inputs, d_num_outputs; // keep track of the topology

     gr::thread::mutex d_mutex;
    
     public:
      selector_39_impl(size_t itemsize, unsigned int input_index, unsigned int output_index);
      ~selector_39_impl() override;

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required) override;
    bool check_topology(int ninputs, int noutputs) override;
    void setup_rpc() override;
    void handle_msg_input_index(pmt::pmt_t msg);
    void handle_msg_output_index(pmt::pmt_t msg);
    void handle_enable(pmt::pmt_t msg);
    void set_enabled(bool enable) override
    {
        gr::thread::scoped_lock l(d_mutex);
        d_enabled = enable;
    }
    bool enabled() const override { return d_enabled; }

    void set_input_index(unsigned int input_index) override;
    int input_index() const override { return d_input_index; }

    void set_output_index(unsigned int output_index) override;
    int output_index() const override { return d_output_index; }

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items) override;
};

  } // namespace itais
} // namespace gr

#endif /* INCLUDED_ITAIS_SELECTOR_39_IMPL_H */


