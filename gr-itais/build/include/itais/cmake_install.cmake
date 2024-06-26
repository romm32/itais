# Install script for directory: /home/gnuradio/gr-itais/include/itais

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/itais" TYPE FILE FILES
    "/home/gnuradio/gr-itais/include/itais/api.h"
    "/home/gnuradio/gr-itais/include/itais/corr_est_cc.h"
    "/home/gnuradio/gr-itais/include/itais/freqest.h"
    "/home/gnuradio/gr-itais/include/itais/invert.h"
    "/home/gnuradio/gr-itais/include/itais/pdu_to_nmea.h"
    "/home/gnuradio/gr-itais/include/itais/msk_timing_recovery_cc.h"
    "/home/gnuradio/gr-itais/include/itais/Build_Frame.h"
    "/home/gnuradio/gr-itais/include/itais/nrz_to_nrzi.h"
    "/home/gnuradio/gr-itais/include/itais/DebugME.h"
    "/home/gnuradio/gr-itais/include/itais/selector_39.h"
    )
endif()

