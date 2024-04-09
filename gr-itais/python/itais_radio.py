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
from gnuradio import zeromq
from gnuradio import analog
import iio


class itais_tx(gr.hier_block2):
    def __init__(self, rate):
        gr.hier_block2.__init__(self,
                                "itais_tx",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(0,0,0))

        # definitions
        self._bits_per_sec = 9600.0
        self._samples_per_symbol = 5
        self.coeffs = filter.firdes.low_pass(1, rate, 11000, 1000)
        self._filter_decimation = int(rate/(self._bits_per_sec*self._samples_per_symbol))
        self.fs = 1000000
        options = {}
        options[ "samples_per_symbol" ] = (rate/self._filter_decimation)/self._bits_per_sec
        options[ "clockrec_gain" ] = 0.04
        options[ "omega_relative_limit" ] = 0.01
        options[ "bits_per_sec" ] = self._bits_per_sec
        options[ "fftlen" ] = 1024 
        options[ "samp_rate" ] = self._bits_per_sec * self._samples_per_symbol

        ### CHANNEL A

        # channel A common blocks and its connections
        self.rational_resampler_A = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=3,
                taps=None,
                fractional_bw=0.4)
        self.filter_A = filter.freq_xlating_fir_filter_ccf(self._filter_decimation,
                                                     self.coeffs,
                                                     -25000, # the center freq is 162 MHz, so this way we sample 161.975 MHz
                                                     rate)
        self.connect(self, self.rational_resampler_A, self.filter_A)
        
        
        # channel A reception blocks
        self.blocks_complex_to_mag_squared_A = blocks.complex_to_mag_squared(1)
        self.potumbral_A = itais.potumbral("A")

        self.connect(self.filter_A, self.blocks_complex_to_mag_squared_A, (self.potumbral_A, 0))
        


        ### CHANNEL B

        # channel B common blocks and its connections
        self.rational_resampler_B = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=3,
                taps=None,
                fractional_bw=0.4)
        self.filter_B = filter.freq_xlating_fir_filter_ccf(self._filter_decimation,
                                                     self.coeffs,
                                                     25000, # the center freq is 162 MHz, so this way we sample 162.025 MHz
                                                     rate)
        self.connect(self, self.rational_resampler_B, self.filter_B)
        
        
        # channel B reception blocks
        self.blocks_complex_to_mag_squared_B = blocks.complex_to_mag_squared(1)
        self.potumbral_B = itais.potumbral("B")

        self.connect(self.filter_B, self.blocks_complex_to_mag_squared_B, (self.potumbral_B, 0))


        ### TRANSMITTER
        self.transmitter = itais.transmitter()
        self.sub_gps = itais.sub_gps()
        self.messages = itais.messages(vessel_length=18, vessel_beam=14, vessel_name="ROMA", vessel_type=30)
        
        self.msg_connect((self.potumbral_A, 'slot_y_puedo'), (self.transmitter, 'slot_y_puedo_A'))
        self.msg_connect((self.potumbral_B, 'slot_y_puedo'), (self.transmitter, 'slot_y_puedo_B'))
        self.connect((self.sub_gps, 1), (self.transmitter, 0)) # se considera la salida con velocidades del sub_gps y la entrada para velocidades del tx

        self.msg_connect((self.transmitter, 'candidatos_A'), (self.potumbral_A, 'candidatos'))
        self.msg_connect((self.transmitter, 'candidatos_B'), (self.potumbral_B, 'candidatos'))
        self.msg_connect((self.transmitter, 'Mensajes'), (self.messages, 'Msg')) # se considera la salida 1 del tx, que avisa qué mensaje es relevante ahora mismo, y la entrada 0 de messages, que recibe pedids de mensajes.

        self.connect((self.sub_gps, 0), (self.messages, 0)) # se considera la salida de un arreglo de cinco valores de sub_gps, y la entrada de messages que recibe esa info.
        

        ### TRANSMISSION        

        self.AISTX_Build_Frame = itais.Build_Frame(True, True, 'packet_len') # me parece que la primera entrada tiene que estar en false para que no se repita la trama enviada?

        self.digital_gmsk_mod = digital.gmsk_mod(int(self.fs/9600), bt=0.4, verbose=False, log=False) #Se fijan los mismos parámetros que en gr-aistx.
        self.selector = itais.selector_39(gr.sizeof_gr_complex*1,0,0)
        self.selector.set_enabled(True)
        self.rational_resampler_tx1 = filter.rational_resampler_ccc(
                  interpolation=5, # interpolamos por 5 y después por 4 para pasar de 50kHz a 1M.
                  decimation=1,
                  taps=None,
                  fractional_bw=0.4)
                  
        self.rational_resampler_tx2 = filter.rational_resampler_ccc(
                  interpolation=4,
                  decimation=1,
                  taps=None,
                  fractional_bw=0.4)
        
        self.blocks_multiply_A = blocks.multiply_vcc(1)
        self.blocks_multiply_B = blocks.multiply_vcc(1)
        self.blocks_multiply_const_A = blocks.multiply_const_cc(0.85)
        self.blocks_multiply_const_B = blocks.multiply_const_cc(0.85)
        self.analog_sig_source_A = analog.sig_source_c(self.fs, analog.GR_SIN_WAVE, -25000, 1, 0, 0)
        self.analog_sig_source_B = analog.sig_source_c(self.fs, analog.GR_SIN_WAVE, 25000, 1, 0, 0) 
                
        self.iio_pluto_sink = iio.pluto_sink('ip:192.168.2.1', 162000000, 1000000, 20000000, 32768, False, 5.0, '', True)
        
        self.msg_connect((self.messages, 'bits_Out'), (self.AISTX_Build_Frame, 'sentence'))
        self.connect((self.AISTX_Build_Frame, 0), (self.digital_gmsk_mod, 0))
                                                #(self.rational_resampler_tx, 0), 
        self.connect((self.digital_gmsk_mod, 0), (self.blocks_multiply_A, 0))
        self.connect((self.digital_gmsk_mod, 0), (self.blocks_multiply_B, 0))

        self.connect((self.analog_sig_source_A, 0), (self.blocks_multiply_A, 1))
        self.connect((self.analog_sig_source_B, 0), (self.blocks_multiply_B, 1))
        
        self.connect((self.blocks_multiply_A, 0), (self.blocks_multiply_const_A, 0))
        self.connect((self.blocks_multiply_B, 0), (self.blocks_multiply_const_B, 0))
        

        self.connect((self.blocks_multiply_const_A, 0), (self.selector, 0))
        self.connect((self.blocks_multiply_const_B, 0), (self.selector, 1))
        self.msg_connect((self.transmitter, 'canal'), (self.selector, 'iindex'))

        self.connect((self.selector, 0), (self.iio_pluto_sink, 0)) 
        

class itais_clase (gr.top_block, pubsub):
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

    self._rx_path = (itais_tx(options.rate))
    self.connect(self._u, self._rx_path)
        

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

        # frecuencia central en 162MHz porque itais_tx (al usar dos canales) directo nos lo traslada a -25kHz y +25kHz.
        src = iio.pluto_source('ip:192.168.2.1', 162000000, 750000, 20000000, 32768, True, True, True, 'manual', 20, '', True)        
        
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
