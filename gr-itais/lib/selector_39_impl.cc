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

 * This file was adapted from the Selector block in GNU Radio 3.9

 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "selector_39_impl.h"
#include <cstring>
#include <stdexcept>
#include <chrono>
#include <iostream>

namespace gr {
  namespace itais {

    selector_39::sptr
    selector_39::make(size_t itemsize, unsigned int input_index, unsigned int output_index)
    {
      return gnuradio::get_initial_sptr
        (new selector_39_impl(itemsize, input_index, output_index));
    }

    /*
     * The private constructor
     */
    selector_39_impl::selector_39_impl(size_t itemsize,
                             unsigned int input_index,
                             unsigned int output_index)
      : gr::block("selector_39",
              gr::io_signature::make(1, -1, itemsize),
              gr::io_signature::make(1, -1, itemsize)),
      d_itemsize(itemsize),
      d_enabled(true),
      d_input_index(input_index),
      d_output_index(output_index),
      d_num_inputs(0),
      d_num_outputs(0)
    {
    message_port_register_in(pmt::mp("en"));
    set_msg_handler(pmt::mp("en"), [this](pmt::pmt_t msg) { this->handle_enable(msg); });
    message_port_register_in(pmt::mp("iindex"));
    set_msg_handler(pmt::mp("iindex"),
                    [this](pmt::pmt_t msg) { this->handle_msg_input_index(msg); });
    message_port_register_in(pmt::mp("oindex"));
    set_msg_handler(pmt::mp("oindex"),
                    [this](pmt::pmt_t msg) { this->handle_msg_output_index(msg); });

    set_tag_propagation_policy(TPP_CUSTOM);
    }



    /*
     * Our virtual destructor.
     */
    selector_39_impl::~selector_39_impl()
    {
    }
    
    void selector_39_impl::set_input_index(unsigned int input_index)
{
    gr::thread::scoped_lock l(d_mutex);
    if (input_index < d_num_inputs)
        d_input_index = input_index;
    else
        throw std::out_of_range("input_index must be < ninputs");
}

void selector_39_impl::set_output_index(unsigned int output_index)
{
    gr::thread::scoped_lock l(d_mutex);
    if (output_index < d_num_outputs)
        d_output_index = output_index;
    else
        throw std::out_of_range("output_index must be < noutputs");
}


void selector_39_impl::handle_enable(pmt::pmt_t msg)
{
    if (pmt::is_bool(msg)) {
        bool en = pmt::to_bool(msg);
        gr::thread::scoped_lock l(d_mutex);
        d_enabled = en;
    } else {
        GR_LOG_WARN(d_logger,
                    "handle_enable: Non-PMT type received, expecting Boolean PMT");
    }
}



void selector_39_impl::handle_msg_input_index(pmt::pmt_t msg)
{
    pmt::pmt_t data = pmt::cdr(msg);

    if (pmt::is_integer(data)) {
        const unsigned int new_port = pmt::to_long(data);
        auto current_time = std::chrono::high_resolution_clock::now();
        auto current_time_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(current_time);
        auto time_since_minute_start = current_time_ns - std::chrono::time_point_cast<std::chrono::minutes>(current_time_ns);
        auto seconds_elapsed = std::chrono::duration_cast<std::chrono::seconds>(time_since_minute_start).count();
        auto milliseconds_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_since_minute_start).count() % 1000;
        auto microseconds_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(time_since_minute_start).count() % 1000;
	std::cout << "Received new port value: " << new_port << " at " << seconds_elapsed << " seconds, " << milliseconds_elapsed << " milliseconds, and " << microseconds_elapsed << " microseconds since the current UTC minute started\n";
        if (new_port < d_num_inputs)
            set_input_index(new_port);
        else
            GR_LOG_WARN(
                d_logger,
                "handle_msg_input_index: port index greater than available ports.");
    } else
        GR_LOG_WARN(
            d_logger,
            "handle_msg_input_index: Non-PMT type received, expecting integer PMT");
}

void selector_39_impl::handle_msg_output_index(pmt::pmt_t msg)
{
    pmt::pmt_t data = pmt::cdr(msg);

    if (pmt::is_integer(data)) {
        const unsigned int new_port = pmt::to_long(data);
        if (new_port < d_num_outputs)
            set_output_index(new_port);
        else
            GR_LOG_WARN(
                d_logger,
                "handle_msg_output_index: port index greater than available ports.");
    } else
        GR_LOG_WARN(
            d_logger,
            "handle_msg_output_index: Non-PMT type received, expecting integer PMT");
}

void selector_39_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    unsigned ninputs = ninput_items_required.size();
    for (unsigned i = 0; i < ninputs; i++) {
        ninput_items_required[i] = 0;
    }
    ninput_items_required[0] = 4096;
    ninput_items_required[1] = 4096;
}


bool selector_39_impl::check_topology(int ninputs, int noutputs)
{
    if ((int)d_input_index < ninputs && (int)d_output_index < noutputs) {
        d_num_inputs = (unsigned int)ninputs;
        d_num_outputs = (unsigned int)noutputs;
        return true;
    } else {
        GR_LOG_WARN(d_logger,
                    "check_topology: Input or Output index greater than number of ports");
        return false;
    }
}

    
    int selector_39_impl::general_work(int noutput_items,
                                gr_vector_int& ninput_items,
                                gr_vector_const_void_star& input_items,
                                gr_vector_void_star& output_items)
{
    const uint8_t** in = (const uint8_t**)&input_items[0];
    uint8_t** out = (uint8_t**)&output_items[0];

    gr::thread::scoped_lock l(d_mutex);
    if (d_enabled) {
        auto nread = nitems_read(d_input_index);
        auto nwritten = nitems_written(d_output_index);

        std::vector<tag_t> tags;
        get_tags_in_window(tags, d_input_index, 0, noutput_items);

        for (auto tag : tags) {
            tag.offset -= (nread - nwritten);
            add_item_tag(d_output_index, tag);
        }
        
        std::copy(in[d_input_index],
                  in[d_input_index] + noutput_items * d_itemsize,
                  out[d_output_index]);
        produce(d_output_index, noutput_items);
    }

    consume_each(noutput_items);
    return WORK_CALLED_PRODUCE;
}


void selector_39_impl::setup_rpc()
{
#ifdef GR_CTRLPORT
    add_rpc_variable(rpcbasic_sptr(new rpcbasic_register_handler<selector_39>(
        alias(), "en", "", "Enable", RPC_PRIVLVL_MIN, DISPNULL)));
#endif /* GR_CTRLPORT */
}

  } /* namespace itais */
} /* namespace gr */



