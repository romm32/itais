
/*
 * This file was automatically generated using swig_doc.py.
 *
 * Any changes to it will be lost next time it is regenerated.
 */




%feature("docstring") gr::itais::Build_Frame "<+description of block+>

Constructor Specific Documentation:

Builds an AIS Frame of 256 bytes.

This module does, in order:

Args:
    repeat : 
    enable_NRZI : 
    lengthtagname : "

%feature("docstring") gr::itais::Build_Frame::make "<+description of block+>

Constructor Specific Documentation:

Builds an AIS Frame of 256 bytes.

This module does, in order:

Args:
    repeat : 
    enable_NRZI : 
    lengthtagname : "

%feature("docstring") gr::itais::corr_est_cc "<+description of block+>

Constructor Specific Documentation:

Make a block that correlates against the  vector and outputs a phase and symbol timing estimate.

Args:
    symbols : Set of symbols to correlate against (e.g., a sync word).
    sps : Samples per symbol
    mark_delay : tag marking delay in samples after the corr_start tag
    threshold : Threshold of correlator, relative to a 100% correlation (1.0). Default is 0.9."





%feature("docstring") gr::itais::corr_est_cc::make "<+description of block+>

Constructor Specific Documentation:

Make a block that correlates against the  vector and outputs a phase and symbol timing estimate.

Args:
    symbols : Set of symbols to correlate against (e.g., a sync word).
    sps : Samples per symbol
    mark_delay : tag marking delay in samples after the corr_start tag
    threshold : Threshold of correlator, relative to a 100% correlation (1.0). Default is 0.9."

%feature("docstring") gr::itais::DebugME "<+description of block+>

Constructor Specific Documentation:

Print the incoming BYTE sequence as sequence of HEXs.

Goes through the incoming sequence (const char *in) and prints it in HEXs

Args:
    itemsize : "

%feature("docstring") gr::itais::DebugME::make "<+description of block+>

Constructor Specific Documentation:

Print the incoming BYTE sequence as sequence of HEXs.

Goes through the incoming sequence (const char *in) and prints it in HEXs

Args:
    itemsize : "

%feature("docstring") gr::itais::freqest "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::freqest.

To avoid accidental use of raw pointers, ais::freqest's constructor is in a private implementation class. ais::freqest::make is the public interface for creating new instances.

Args:
    sample_rate : 
    data_rate : 
    fftlen : "

%feature("docstring") gr::itais::freqest::make "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::freqest.

To avoid accidental use of raw pointers, ais::freqest's constructor is in a private implementation class. ais::freqest::make is the public interface for creating new instances.

Args:
    sample_rate : 
    data_rate : 
    fftlen : "

%feature("docstring") gr::itais::invert "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::invert.

To avoid accidental use of raw pointers, ais::invert's constructor is in a private implementation class. ais::invert::make is the public interface for creating new instances."

%feature("docstring") gr::itais::invert::make "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::invert.

To avoid accidental use of raw pointers, ais::invert's constructor is in a private implementation class. ais::invert::make is the public interface for creating new instances."

%feature("docstring") gr::itais::msk_timing_recovery_cc "<+description of block+>

Constructor Specific Documentation:

Make an MSK timing recovery block.

Args:
    sps : Samples per symbol
    gain : Loop gain of timing error filter (try 0.05)
    limit : Relative limit of timing error (try 0.1 for 10% error max)
    osps : Output samples per symbol"













%feature("docstring") gr::itais::msk_timing_recovery_cc::make "<+description of block+>

Constructor Specific Documentation:

Make an MSK timing recovery block.

Args:
    sps : Samples per symbol
    gain : Loop gain of timing error filter (try 0.05)
    limit : Relative limit of timing error (try 0.1 for 10% error max)
    osps : Output samples per symbol"

%feature("docstring") gr::itais::nrz_to_nrzi "<+description of block+>

Constructor Specific Documentation:

Convert from NRZ to NRZI.

Convert a BYTE sequence from NRZ to NRZI. Note: This is also implemented in the Build_Frame component."

%feature("docstring") gr::itais::nrz_to_nrzi::make "<+description of block+>

Constructor Specific Documentation:

Convert from NRZ to NRZI.

Convert a BYTE sequence from NRZ to NRZI. Note: This is also implemented in the Build_Frame component."

%feature("docstring") gr::itais::pdu_to_nmea "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::pdu_to_nmea.

To avoid accidental use of raw pointers, ais::pdu_to_nmea's constructor is in a private implementation class. ais::pdu_to_nmea::make is the public interface for creating new instances.

Args:
    designator : "





%feature("docstring") gr::itais::pdu_to_nmea::make "<+description of block+>

Constructor Specific Documentation:

Return a shared_ptr to a new instance of ais::pdu_to_nmea.

To avoid accidental use of raw pointers, ais::pdu_to_nmea's constructor is in a private implementation class. ais::pdu_to_nmea::make is the public interface for creating new instances.

Args:
    designator : "

%feature("docstring") gr::itais::selector_39 "<+description of block+>

Constructor Specific Documentation:



Args:
    itemsize : 
    input_index : 
    output_index : "













%feature("docstring") gr::itais::selector_39::make "<+description of block+>

Constructor Specific Documentation:



Args:
    itemsize : 
    input_index : 
    output_index : "

%feature("docstring") modulate_vector_bc "Modulate a vector of data and apply a shaping filter.

Pointer to a byte-to-complex modulator block.  Vector of bytes to modulate into symbols.  Post-modulation symbol shaping filter taps.


This function modulates the input vector and applies a symbol shaping filter. It is intended for use with the corr_est_cc block as the symbol stream to correlate against.


Any differential encoding or other data coding must be performed on the input vector before this modulation operation.


Be aware that the format of the incoming data must match the format the modulator block is expecting. GNURadio modulator blocks are inconsistent in their data type expectations. For instance, cpmmod_bc expects unpacked, signed bytes in (-1, 1), while gmsk_mod expects packed, unsigned bytes in (0, 1). In other words, the output of gmsk_mod given the input vector [0xaa, 0x00] is equivalent to the output of cpmmod_bc given the input vector [1,255,1,255,1,255,1,255,255,255,255,255,255,255,255,255]


Please check the documentation or source of the modulator before using this function."