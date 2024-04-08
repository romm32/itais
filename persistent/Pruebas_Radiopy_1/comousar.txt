En esta carpeta se tienen:

	-prueba-radiopy.py: un script que, mientras se ejecuta el receptor de gr-ais, permite obtener las muestras recibidas del canal (luego de filtradas) y enviarlas a un archivo txt.
	-taps.txt: archivo .txt donde se guardan las muestras. En general es pesado y tarda en abrir, además de que no es "legible" al abrirlo con gedit o cat (probablemente porque no está codificado en UTF-8 o algo similar).
	-lectura-taps.py: script de python que permite leer las muestras del archivo taps.txt e imprimir los primeros diez valores en la terminal.
	
Como se mencionó previamente, para que prueba-radiopy.py funcione de forma correcta, debe estarse ejecutando en el background el script de radio.py de gr-ais. 

Al momento de probar este archivo, la configuración extra realizada en radio.py es la siguient (destacando en mayúsculas y con muchos asteriscos los cambios).

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



######################## AGREGADO DE UN SEGUNDO FILTRO ANÁLOGO AL PRIMERO PARA EL DESVÍO DE LAS MUESTRAS
                                                     
        self.filter2 = filter.freq_xlating_fir_filter_ccf(self._filter_decimation,
                                                     self.coeffs,
                                                     freq,
                                                     rate)     
########################
                                                     
#        self.resamp = pfb.arb_resampler_ccf((self._bits_per_sec*self._samples_per_symbol)/int(rate/self._filter_decimation))
        options = {}
        options[ "samples_per_symbol" ] = (rate/self._filter_decimation)/self._bits_per_sec
        options[ "clockrec_gain" ] = 0.04
        options[ "omega_relative_limit" ] = 0.01
        options[ "bits_per_sec" ] = self._bits_per_sec
        options[ "fftlen" ] = 1024 #trades off accuracy of freq estimation in presence of noise, vs. delay time.
        options[ "samp_rate" ] = self._bits_per_sec * self._samples_per_symbol
        self.demod = ais.ais_demod(options) #ais_demod takes in complex baseband and spits out 1-bit unpacked bitstream
        self.deframer = digital.hdlc_deframer_bp(11,64) #takes bytes, deframes, unstuffs, CRCs, and emits PDUs with frame contents
        self.nmea = ais.pdu_to_nmea(designator) #turns data PDUs into NMEA sentences
        
        print("El designador es:", designator)

#        self.msgq = ais.pdu_to_msgq(queue) #posts PDUs to message queue for main program to parse at will
#        self.parse = ais.parse(queue, designator) #ais_parse.cc, calculates CRC, parses data into NMEA AIVDM message, moves data onto queue
        
######################## AGREGADO DE BLOQUES ZMQ, UNO PARA CADA CANAL, Y CONEXIÓN DEL FILTRO CON DICHO BLOQUE.
        ##Empiezan modifs
        # Create a ZMQ Pub block
        if (designator == "A"):
            self.zmq_pub = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5555', 100, False, -1)
        else:
            self.zmq_pub = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5556', 100, False, -1)

        
        self.connect(self, self.filter2, (self.zmq_pub, 0))
        
########################        

        self.connect(self,
                     self.filter,
                     self.demod,
                     self.deframer)
        self.msg_connect(self.deframer, "out", self.nmea, "print")
