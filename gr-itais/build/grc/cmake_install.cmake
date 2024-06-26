# Install script for directory: /home/gnuradio/gr-itais/grc

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/gnuradio/gr-itais/grc/itais_messages.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_sub_gps.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_transmitter.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_potumbral.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_gmsk_sync.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_ais_demod.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_corr_est_cc.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_freqest.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_invert.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_pdu_to_nmea.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_msk_timing_recovery_cc.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_Build_Frame.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_nrz_to_nrzi.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_DebugME.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_selector_itais.block.yml"
    "/home/gnuradio/gr-itais/grc/itais_selector_39.block.yml"
    )
endif()

