/* -*- c++ -*- */
/*
 * Copyright 2024 trendmicro, bmagistro. Modified in the ITAIS project.
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


#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "Build_Frame_impl.h"
#include <gnuradio/blocks/pdu.h>
#include <gnuradio/io_signature.h>
#include <gnuradio/tagged_stream_block.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <chrono>

#define LEN_PREAMBLE 24
#define LEN_START 8
#define LEN_CRC 16
#define LEN_FRAME_MAX 256

#define PREAMBLE_MARK 101010101010101010101010(24 bits)
#define START_MARK 01111110(8 bits)

#define PREAMBLE_MARK_ZERO 000000000000000000000000(24 bits)
#define START_MARK_ZERO 00000000(8 bits)

#define DEBUG 0

namespace gr {
namespace itais {

Build_Frame::sptr
Build_Frame::make(bool repeat, bool enable_NRZI, const std::string& tsb_tag_key)
{
    return gnuradio::get_initial_sptr(
        new Build_Frame_impl(repeat, enable_NRZI, tsb_tag_key));
}

/*
 * The private constructor
 */
Build_Frame_impl::Build_Frame_impl(bool repeat,
                                   bool enable_NRZI,
                                   const std::string& tsb_tag_key)
    : gr::tagged_stream_block("Build_Frame",
                              gr::io_signature::make(0, 0, 0),
                              gr::io_signature::make(1, 1, sizeof(unsigned char)),
                              tsb_tag_key),
      d_repeat(repeat),
      d_repeat_cnt(0),
      d_enable_NRZI(enable_NRZI),
      d_itemsize(sizeof(unsigned char)),
      d_curr_len(0)
{
    message_port_register_in(pmt::mp("sentence"));
}


void Build_Frame_impl::dump_buffer(const char* b, int buffer_size)
{
    int k = 0;
    for (; k < buffer_size; k++)
        printf("%d", b[k]);
    printf("\n");
}

// buffer must have length >= sizeof(int) + 1
// Write to the buffer backwards so that the binary representation
// is in the correct order i.e.  the LSB is on the far right
// instead of the far left of the printed string
char* Build_Frame_impl::int2bin(int a, char* buffer, int buf_size)
{
    buffer += (buf_size - 1);

    for (int i = 31; i >= 0; i--) {
        *buffer-- = (a & 1) + '0';

        a >>= 1;
    }

    return buffer;
}

// stuffing function
int Build_Frame_impl::stuff(const char* in, char* out, int l_in)
{
    int i = 0, j = 0, consecutives = 0, l_out = 0;

    while (i < l_in) {

        if (in[i] & 0x01)
            consecutives++;
        else
            consecutives = 0;

        out[j++] = in[i++];
        l_out++;

        if (consecutives == 5) {
            out[j++] = 0x0;
            l_out++;
            consecutives = 0;
        }
    }
    return l_out;
}

void Build_Frame_impl::pack(int orig_ascii, char* ret, int bits_per_byte)
{
    // go down to fit in 6 bits
    int ascii = orig_ascii - 48;
    if (ascii > 39)
        ascii -= 8;

    char binary[6];
    int y = 0;

    if (ascii == 0)
        memset(binary, 0x0, 6);
    else
        while (ascii != 1) {
            if (ascii % 2 == 0)
                binary[y] = 0x0;
            else if (ascii % 2 == 1)
                binary[y] = 0x1;
            ascii /= 2;
            y++;
        }

    if (ascii == 1) {
        binary[y] = 0x1;
        y++;
    }

    if (y < 6) { // fill in space
        for (; y < 6; y++)
            binary[y] = 0x0;
    }

    for (y = 0; y < 6; y++) // reverse*/
        ret[y] = binary[5 - y];
    ret[y] = '\0';

}

void Build_Frame_impl::nrz_to_nrzi(char* data, int length)
{
    unsigned short d_prev_nrzi_bit = 0;
    unsigned short nrz_bit, nrzi_bit;

    for (int i = 0; i < length; i++) {
        nrz_bit = data[i];

        if (nrz_bit == 0) {
            nrzi_bit = d_prev_nrzi_bit ^ 1;
        } else {
            nrzi_bit = d_prev_nrzi_bit;
        }

        data[i] = nrzi_bit;
        d_prev_nrzi_bit = nrzi_bit;
    }
}

void Build_Frame_impl::reverse_bit_order(char* data, int length)
{
    int tmp = 0;
    for (int i = 0; i < length / 8; i++) {
        for (int j = 0; j < 4; j++) {
            tmp = data[i * 8 + j];
            data[i * 8 + j] = data[i * 8 + 7 - j];
            data[i * 8 + 7 - j] = tmp;
        }
    }
}

unsigned long Build_Frame_impl::unpack(char* buffer, int start, int length)
{
    unsigned long ret = 0;
    for (int i = start; i < (start + length); i++) {
        ret <<= 1;
        ret |= (buffer[i] & 0x01);
    }
    return ret;
}

void Build_Frame_impl::compute_crc(
    char* buffer,
    char* ret,
    unsigned int len) // Calculates CRC-checksum from unpacked data
{
    // clang-format off
    static const unsigned short crc_itu16_table[] = {
        0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
        0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
        0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
        0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
        0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
        0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
        0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
        0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
        0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
        0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
        0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
        0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
        0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
        0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
        0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
        0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
        0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
        0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
        0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
        0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
        0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
        0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
        0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
        0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
        0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
        0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
        0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
        0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
        0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
        0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
        0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
        0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
    };
    // clang-format on

    int crc = 0xffff;
    int i = 0;
    char temp[8];
    int datalen = len / 8;

    char data[256];
    // this unpacks the data in preparation for calculating CRC
    for (int j = 0; j < datalen; j++) {
        data[j] = unpack(buffer, j * 8, 8);
    }

    for (i = 0; i < datalen; i++)
        crc = (crc >> 8) ^ crc_itu16_table[(crc ^ data[i]) & 0xFF];

    crc = (crc & 0xFFFF) ^ 0xFFFF;

    int2bin(crc, ret, 16);

    reverse_bit_order(ret, 16); // revert crc bit in byte

    int2bin(crc, ret, 16);
    strncpy(temp, ret + 8, 8); // swap the two crc byte
    strncpy(ret + 8, ret, 8);
    strncpy(ret, temp, 8);

    // back to binary
    for (int j = 0; j < 16; j++)
        ret[j] = ret[j] - 0x30;

}

void Build_Frame_impl::byte_packing(char* input_frame,
                                    unsigned char* out_byte,
                                    unsigned int len)
{
    for (int i = 0; i < len / 8; i++) {
        char tmp[8];
        memcpy(tmp, &input_frame[i * 8], 8);
        out_byte[i] = tmp[0] * 128 + tmp[1] * 64 + tmp[2] * 32 + tmp[3] * 16 +
                      tmp[4] * 8 + tmp[5] * 4 + tmp[6] * 2 + tmp[7];

    }
}

int Build_Frame_impl::calculate_output_stream_length(const gr_vector_int& ninput_items)
{
    // straight copy from `pdu to tagged stream block`
    if (d_curr_len == 0) {
        pmt::pmt_t msg(delete_head_nowait(pmt::mp("sentence")));
        if (msg.get() == NULL) {
            return 0;
        }

        if (pmt::is_pair(msg)) {
            d_curr_meta = pmt::car(msg);
            d_curr_vect = pmt::cdr(msg);
            // do not assume the length of  PMT is in items (e.g.: from socket_pdu)
            d_curr_len = pmt::blob_length(d_curr_vect) / d_itemsize;
        } else if (pmt::is_symbol(msg)) {
            // transform a symbol to a uniform vector
            const std::string sym_str = symbol_to_string(msg);
            d_curr_vect = pmt::init_u8vector(
                sym_str.length(), reinterpret_cast<const uint8_t*>(sym_str.c_str()));
            d_curr_len = sym_str.length();
        } else {
            throw std::runtime_error(
                "received a message type that hasn't been implemented");
        }
    }

    return d_curr_len;
}

int Build_Frame_impl::work(int noutput_items,
                           gr_vector_int& ninput_items,
                           gr_vector_const_void_star& input_items,
                           gr_vector_void_star& output_items)
{
    // some direct copies in here from `pdu to tagged stream block` too
    // sleep at the start, if we stop too quickly after the send, the send doesn't seem to
    // happen
    usleep(100000);

    // if not set to repeat and we've sent a message we can exit
    if (!d_repeat && d_repeat_cnt > 0) {
        return WORK_DONE;
    }

    char* out = (char*)output_items[0];

    if (d_curr_len == 0) {
        return 0;
    }

    // work() should only be called if the current PDU fits entirely
    // into the output buffer.
    assert(noutput_items >= 0 && (unsigned int)noutput_items >= d_curr_len);

    // Copy vector output
    size_t nout = d_curr_len;
    size_t io(0);
    const uint8_t* ptr = (const uint8_t*)uniform_vector_elements(d_curr_vect, io);
    memcpy(out, ptr, d_curr_len * d_itemsize);

    // at this point we have the `sentence` stored in `out` and length in `nout`.
    // printf("len: %ld; val: %s\n", nout, out);
    // printf("buf len: %ld; in lenL %ld\n", noutput_items, ninput_items);
    // TODO get a better understanding of noutput_items, set at 32768, but not entirely
    //   sure where/how had been under the impression this would be based on the
    //   calc length function but it does not seem related.
    //   going off the 32k, our output should always fit..

    // char* d_sentence;
    const char* sentence = out;
    char* payload; // [the 01 rapresentation of the sentence as taken from input]
    unsigned short LEN_SENTENCE;
    unsigned short LEN_PAYLOAD;

    unsigned short REMAINDER_TO_EIGHT,
        PADDING_TO_EIGHT; // to pad the payload to a multiple of 8

    LEN_PAYLOAD = strlen(sentence);
    if (LEN_PAYLOAD > 168)
        printf("Frame padding disabled. Multiple packets.\n");

    // IMPORTANT
    REMAINDER_TO_EIGHT = LEN_PAYLOAD % 8;
    if (REMAINDER_TO_EIGHT == 0) {
        payload = (char*)malloc(LEN_PAYLOAD + LEN_CRC);
        // nb. It comes in in ASCII
        for (int i = 0; i < LEN_PAYLOAD; i++)
            payload[i] = sentence[i] - 48;
    } else if (REMAINDER_TO_EIGHT > 0) {

        PADDING_TO_EIGHT = 8 - REMAINDER_TO_EIGHT;
        payload = (char*)malloc(LEN_PAYLOAD + PADDING_TO_EIGHT + LEN_CRC);

        for (int i = 0; i < LEN_PAYLOAD; i++)
            payload[i] = sentence[i] - 48;

        memset(payload + LEN_PAYLOAD, 0x0, PADDING_TO_EIGHT);

        LEN_PAYLOAD += PADDING_TO_EIGHT; // update PAYLOAD LENGHT
    }

    // crc
    char crc[16]; // 2 gnuradio bytes of CRC
    char input_crc[LEN_PAYLOAD];
    memcpy(input_crc, payload, LEN_PAYLOAD);
    compute_crc(input_crc, crc, LEN_PAYLOAD);
    memcpy(payload + LEN_PAYLOAD, crc, LEN_CRC);

    // reverse
    reverse_bit_order(payload, LEN_PAYLOAD + LEN_CRC);

    // stuffing (payload + crc)
    
    // generation of dummy message
    if (LEN_PAYLOAD == 155) {
        char stuffed_payload[LEN_FRAME_MAX];
        int LEN_STUFFED_PAYLOAD = stuff(payload, stuffed_payload, LEN_PAYLOAD + LEN_CRC);

        //// frame generation /////
        char frame[LEN_FRAME_MAX];
        unsigned char byte_frame[LEN_FRAME_MAX / 8]; // PASTA
        memset(frame, 0x0, LEN_FRAME_MAX);

        // headers
        memcpy(frame, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", LEN_PREAMBLE);
        memcpy(frame + LEN_PREAMBLE, "\0\0\0\0\0\0\0\0", LEN_START);
        // payload + crc
        memcpy(frame + LEN_PREAMBLE + LEN_START, stuffed_payload, LEN_STUFFED_PAYLOAD);
        // trailer
        memcpy(frame + LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD,
            "\0\0\0\0\0\0\0\0",
            8);

        // padding
        int LEN_PADDING =
            LEN_FRAME_MAX - (LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD + LEN_START);
        memset(frame + LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD + LEN_START,
            0x0,
            LEN_PADDING);
        int len_frame_real = LEN_FRAME_MAX; // 256

        // NRZI Conversion
        nrz_to_nrzi(frame, len_frame_real);
        //printf("Sent Frame (NRZI enabled) = ");
        auto current_time = std::chrono::high_resolution_clock::now();
        auto current_time_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(current_time);
        auto time_since_minute_start = current_time_ns - std::chrono::time_point_cast<std::chrono::minutes>(current_time_ns);
        auto seconds_elapsed = std::chrono::duration_cast<std::chrono::seconds>(time_since_minute_start).count();
        auto milliseconds_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_since_minute_start).count() % 1000;
        auto microseconds_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(time_since_minute_start).count() % 1000;
        std::cout << "Sent dummy message\n"; //<< seconds_elapsed << " seconds, " << milliseconds_elapsed << " milliseconds, and " << microseconds_elapsed << " microseconds since the current UTC minute started\n";

        // Binary conversion (to use with GMSK mod's byte_to_symb
        byte_packing(frame, byte_frame, len_frame_real);

        // output
        memcpy(out, byte_frame, len_frame_real / 8);
        noutput_items = len_frame_real / 8;
        
        d_repeat_cnt++;
        // Reset state
        d_curr_len = 0;

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }
    
    else {
        if (LEN_PAYLOAD <= 168) {
            char stuffed_payload[LEN_FRAME_MAX];
            int LEN_STUFFED_PAYLOAD = stuff(payload, stuffed_payload, LEN_PAYLOAD + LEN_CRC);

            //// frame generation /////
            char frame[LEN_FRAME_MAX];
            unsigned char byte_frame[LEN_FRAME_MAX / 8]; // PASTA
            memset(frame, 0x0, LEN_FRAME_MAX);

            // headers. Preamble must begin with 0 in CSTDMA
            memcpy(frame, "\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1", LEN_PREAMBLE);
            memcpy(frame + LEN_PREAMBLE, "\0\1\1\1\1\1\1\0", LEN_START);
            // payload + crc
            memcpy(frame + LEN_PREAMBLE + LEN_START, stuffed_payload, LEN_STUFFED_PAYLOAD);
            // trailer
            memcpy(frame + LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD,
                "\0\1\1\1\1\1\1\0",
                8);

            // padding
            int LEN_PADDING =
                LEN_FRAME_MAX - (LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD + LEN_START);
            memset(frame + LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD + LEN_START,
                0x0,
                LEN_PADDING);
            int len_frame_real = LEN_FRAME_MAX; // 256

            // NRZI Conversion
            nrz_to_nrzi(frame, len_frame_real);
            //printf("Sent Frame (NRZI enabled) = ");
            auto current_time = std::chrono::high_resolution_clock::now();
            auto current_time_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(current_time);
            auto time_since_minute_start = current_time_ns - std::chrono::time_point_cast<std::chrono::minutes>(current_time_ns);
            auto seconds_elapsed = std::chrono::duration_cast<std::chrono::seconds>(time_since_minute_start).count();
            auto milliseconds_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_since_minute_start).count() % 1000;
            auto microseconds_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(time_since_minute_start).count() % 1000;
            std::cout << "Sent new message.\n";// << seconds_elapsed << " seconds, " << milliseconds_elapsed << " milliseconds, and " << microseconds_elapsed << " microseconds since the current UTC minute started\n";

            // Binary conversion (to use with GMSK mod's byte_to_symb
            byte_packing(frame, byte_frame, len_frame_real);

            // output
            memcpy(out, byte_frame, len_frame_real / 8);
            noutput_items = len_frame_real / 8;
        } 
    
        else {
            char stuffed_payload[1024];
            int LEN_STUFFED_PAYLOAD = stuff(payload, stuffed_payload, LEN_PAYLOAD + LEN_CRC);

            //// frame generation /////
            int LEN_FRAME = LEN_PREAMBLE + LEN_START * 2 + LEN_STUFFED_PAYLOAD;
            char frame[LEN_FRAME];
            unsigned char byte_frame[LEN_FRAME / 8]; // PASTA
            memset(frame, 0x0, LEN_FRAME);

            // headers. Preamble must begin with 0 in CSTDMA
            memcpy(frame, "\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1\0\1", LEN_PREAMBLE);
            memcpy(frame + LEN_PREAMBLE, "\0\1\1\1\1\1\1\0", LEN_START);
            // payload + crc
            memcpy(frame + LEN_PREAMBLE + LEN_START, stuffed_payload, LEN_STUFFED_PAYLOAD);
            // trailer
            memcpy(frame + LEN_PREAMBLE + LEN_START + LEN_STUFFED_PAYLOAD,
                "\0\1\1\1\1\1\1\0",
                8);

            int len_frame_real = LEN_FRAME;

            // NRZI Conversion
            nrz_to_nrzi(frame, len_frame_real);
            //printf("Sent Frame (NRZI enabled) = ");

            auto current_time = std::chrono::high_resolution_clock::now();
            auto current_time_ns = std::chrono::time_point_cast<std::chrono::nanoseconds>(current_time);
            auto time_since_minute_start = current_time_ns - std::chrono::time_point_cast<std::chrono::minutes>(current_time_ns);
            auto seconds_elapsed = std::chrono::duration_cast<std::chrono::seconds>(time_since_minute_start).count();
            auto milliseconds_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(time_since_minute_start).count() % 1000;
            auto microseconds_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(time_since_minute_start).count() % 1000;
            std::cout << "Sent new message.\n"; // << seconds_elapsed << " seconds, " << milliseconds_elapsed << " milliseconds, and " << microseconds_elapsed << " microseconds since the current UTC minute started\n";

            // Binary conversion (to use with GMSK mod's byte_to_symb
            byte_packing(frame, byte_frame, len_frame_real);

            // output
            memcpy(out, byte_frame, len_frame_real / 8);
            noutput_items = len_frame_real / 8;
        }

        d_repeat_cnt++;
        // Reset state
        d_curr_len = 0;

        // return nout;


        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

} /* namespace AISTX */
} /* namespace gr */
}


