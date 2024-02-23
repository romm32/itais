# Copyright 2013 Nick Foster
# 
# This file is part of gr-ais
# 
# gr-ais is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# gr-ais is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with gr-ais; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

# Radio interface for AIS receiver
# Handles all hardware- and source-related functionality
# You pass it options, it gives you data.
# It uses the pubsub interface to allow clients to subscribe to its data feeds.

from gnuradio import gr, gru, eng_notation, filter, blocks, digital
from gnuradio.filter import optfir
from gnuradio.filter import pfb
from gnuradio.eng_option import eng_option
from gnuradio.gr.pubsub import pubsub
from optparse import OptionParser, OptionGroup
import threading
import time
import sys
import re
import itais
import potumbral 
#import igualarpotencias
from gnuradio import zeromq
import example

#hier block encapsulating all the signal processing after the source
#could probably be split into its own file
class ais_rx(gr.hier_block2):
    def __init__(self, freq, rate, designator):
        gr.hier_block2.__init__(self,
                                "ais_rx",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(0,0,0))

        self._bits_per_sec = 9600.0
        self._samples_per_symbol = 5
        self.coeffs = filter.firdes.low_pass(1, rate, 11000, 1000)
        self._filter_decimation = int(rate/(self._bits_per_sec*self._samples_per_symbol))
        self.filter = filter.freq_xlating_fir_filter_ccf(self._filter_decimation,
                                                     self.coeffs,
                                                     freq,
                                                     rate)
                                                     
        self.filter2 = filter.freq_xlating_fir_filter_ccf(self._filter_decimation,
                                                     self.coeffs,
                                                     freq,
                                                     rate)     
#        self.resamp = pfb.arb_resampler_ccf((self._bits_per_sec*self._samples_per_symbol)/int(rate/self._filter_decimation))
        options = {}
        options[ "samples_per_symbol" ] = (rate/self._filter_decimation)/self._bits_per_sec
        options[ "clockrec_gain" ] = 0.04
        options[ "omega_relative_limit" ] = 0.01
        options[ "bits_per_sec" ] = self._bits_per_sec
        options[ "fftlen" ] = 1024 #trades off accuracy of freq estimation in presence of noise, vs. delay time.
        options[ "samp_rate" ] = self._bits_per_sec * self._samples_per_symbol
        self.demod = itais.ais_demod(options) #ais_demod takes in complex baseband and spits out 1-bit unpacked bitstream
        self.deframer = digital.hdlc_deframer_bp(11,64) #takes bytes, deframes, unstuffs, CRCs, and emits PDUs with frame contents
        self.nmea = itais.pdu_to_nmea(designator) #turns data PDUs into NMEA sentences
        
        print("El designador es:", designator)
        
        ##Empiezan modifs
        # Create a ZMQ Pub block
        if (designator == "A"):
            self.zmq_pub = zeromq.pub_sink(gr.sizeof_float, 2, 'tcp://127.0.0.1:5610', 1, False, -1)
            self.zmq_sub = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5605', 1, False, -1)
        else:
            self.zmq_pub = zeromq.pub_sink(gr.sizeof_float, 2, 'tcp://127.0.0.1:5611', 1, False, -1)
            self.zmq_sub = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5606', 1, False, -1)
            

        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*2, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 10)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        
        #self.example_tag_to_msg_0 = example.tag_to_msg(gr.sizeof_float*1, '', "latency_strobe")
        #self.example_latency_manager_0 = example.latency_manager(2000, 1000, gr.sizeof_float*1)


        #self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, rate,True)
        #self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(1/((2**15)-1))
        
        self.potumbral = itais.potumbral(designator)
        
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=3,
                taps=None,
                fractional_bw=0.4)
                
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=3,
                taps=None,
                fractional_bw=0.4)
        
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        
        self.connect(self, (self.rational_resampler_xxx_0, 0), self.filter2,  self.blocks_complex_to_mag_squared_0, (self.potumbral, 0)) #self.example_latency_manager_0, (self.potumbral, 0))
        #self.msg_connect((self.example_tag_to_msg_0, 'msg'), (self.example_latency_manager_0, 'token'))
        #self.connect((self.potumbral, 0), self.example_tag_to_msg_0)
        
        
        self.connect((self.potumbral, 0), (self.blocks_vector_to_stream_0, 0), (self.zmq_pub, 0))
        #self.connect((self.potumbral, 0), (self.zmq_pub, 0))
        self.connect((self.zmq_sub, 0), (self.blocks_stream_to_vector_0, 0), (self.potumbral, 1))
      
        self.connect(self, self.rational_resampler_xxx_1,             
                     self.filter,
                     self.demod,
                     self.deframer)
        self.msg_connect(self.deframer, "out", self.nmea, "print")

class ais_radio (gr.top_block, pubsub):
  def __init__(self, options):
    gr.top_block.__init__(self)
    pubsub.__init__(self)
    self._options = options

    self._u = self._setup_source(options)
    if options.source == "pluto":
    	self._rate = 750000/3 # el pluto necesita que usemos un sample rate mayor a 500kHz aprox, entonces usamos 750kHz. Luego lo dividimos entre 3 en el flujo de datos usando un rationalresampler, pero a los efectos de todas las veces que se usa la variable rate, tiene sentido inicializarla como 250kHz.
    else:
    	self._rate = self.get_rate()
    #self._rate = self.get_rate()
    print("Rate is %i" % (self._rate,))

    if options.singlechannel is True:
        self._rx_paths = (ais_rx(0, options.rate, "A"),)
    else:
        self._rx_paths = (ais_rx(161.975e6 - 162.0e6, options.rate, "A"),
                          ais_rx(162.025e6 - 162.0e6, options.rate, "B"))
    for rx_path in self._rx_paths:
        self.connect(self._u, rx_path)

    #now subscribe to set various options via pubsub
    self.subscribe("gain", self.set_gain)
    self.subscribe("rate", self.set_rate)

    self.publish("gain", self.get_gain)
    self.publish("rate", self.get_rate)

  @staticmethod
  def add_radio_options(parser):
    group = OptionGroup(parser, "Receiver setup options")

    #Choose source
    group.add_option("-s","--source", type="string", default="uhd",
                      help="Choose source: uhd, osmocom, pluto, <filename>, or <ip:port> [default=%default]")

    #UHD/Osmocom args
    group.add_option("-R", "--subdev", type="string",
                      help="select USRP Rx side A or B", metavar="SUBDEV")
    group.add_option("-A", "--antenna", type="string",
                      help="select which antenna to use on daughterboard")
    group.add_option("-D", "--args", type="string",
                      help="arguments to pass to radio constructor", default="")
    group.add_option("-g", "--gain", type="int", default=None,
                      help="set RF gain", metavar="dB")
    parser.add_option("-e", "--error", type="eng_float", default=0,
                        help="set offset error of device in PPM [default=%default]")
    #RX path args
    group.add_option("-r", "--rate", type="eng_float", default=250e3,
                      help="set sample rate [default=%default]")
    group.add_option("-S", "--singlechannel", action="store_true", default=False,
                     help="Use only a single channel instead of looking at both A & B [default=%default]")

    parser.add_option_group(group)

  def live_source(self):
    return self._options.source=="uhd" or self._options.source=="osmocom" or self._options.source=="pluto"

  def set_gain(self, gain):
    if self.live_source():
        self._u.set_gain(gain)
        print("Gain is %f" % self.get_gain())
    return self.get_gain()

  def set_rate(self, rate):
    for rx_path in self._rx_paths:
        rx_path1.set_rate(rate)
    return self._u.set_rate(rate) if self.live_source() else self._rate

  def set_threshold(self, threshold):
    for rx_path in self._rx_paths:
        rx_path.set_threshold(threshold)

  def get_gain(self):
    return self._u.get_gain() if self.live_source() else 0

  def get_rate(self):
    return self._u.get_samp_rate() if self.live_source() else self._rate

  def _setup_source(self, options):
    if options.source == "uhd":
      #UHD source by default
      from gnuradio import uhd
      src = uhd.usrp_source(options.args, uhd.stream_args(cpu_format="fc32", channels=range(1)))

      if(options.subdev):
        src.set_subdev_spec(options.subdev, 0)

      if not src.set_center_freq(162.0e6 * (1 + options.error/1.e6)):
        print("Failed to set initial frequency")
      else:
        print("Tuned to %.3fMHz" % (src.get_center_freq() / 1.e6))

      #check for GPSDO
      #if you have a GPSDO, UHD will automatically set the timestamp to UTC time
      #as well as automatically set the clock to lock to GPSDO.
      if src.get_time_source(0) != 'gpsdo':
        src.set_time_now(uhd.time_spec(0.0))

      if options.antenna is not None:
        src.set_antenna(options.antenna)

      src.set_samp_rate(options.rate)

      if options.gain is None: #set to halfway
        g = src.get_gain_range()
        options.gain = (g.start()+g.stop()) / 2.0

      print("Setting gain to %i" % options.gain)
      src.set_gain(options.gain)
      print("Gain is %i" % src.get_gain())

    #TODO: detect if you're using an RTLSDR or Jawbreaker
    #and set up accordingly.
    elif options.source == "osmocom": #RTLSDR dongle or HackRF Jawbreaker
        import osmosdr
        src = osmosdr.source(options.args)
        src.set_sample_rate(options.rate)
        src.get_samp_rate = src.get_sample_rate #alias for UHD compatibility
        if not src.set_center_freq(162.0e6 * (1 + options.error/1.e6)):
            print("Failed to set initial frequency")
        else:
            print("Tuned to %.3fMHz" % (src.get_center_freq() / 1.e6))

        if options.gain is None:
            options.gain = 34
        src.set_gain(options.gain)
        print("Gain is %i" % src.get_gain())
        
    elif options.source == "pluto": #adalm pluto 
        import iio
        #src = iio.pluto_source()
        # frecuencia central en 162MHz porque ais_rx (al usar dos canales) directo nos lo traslada a -25kHz y +25kHz.
        src = iio.pluto_source('ip:192.168.2.1', 162000000, 750000, 20000000, 32768, True, True, True, 'manual', 20, '', True)
        #src.get_samp_rate = src.get_sample_rate #alias for UHD compatibility
        
        
    else:
      #semantically detect whether it's ip.ip.ip.ip:port or filename
      self._rate = options.rate
      if ':' in options.source:
        try:
          ip, port = re.search("(.*)\:(\d{1,5})", options.source).groups()
        except:
          raise Exception("Please input UDP source e.g. 192.168.10.1:12345")
        payload_size = 8972
        src = blocks.udp_source(gr.sizeof_short*1, ip, int(port),payload_size,True)
        print("Using UDP source %s:%s and Payload Size %s" % (ip, port,payload_size))
      else:
        src = blocks.file_source(gr.sizeof_gr_complex, options.source)
        print("Using file source %s" % options.source)

    return src

  def close(self):
    src = None
