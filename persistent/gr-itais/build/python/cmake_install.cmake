# Install script for directory: /home/gnuradio/gr-itais/python

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/itais" TYPE FILE FILES
    "/home/gnuradio/gr-itais/python/__init__.py"
    "/home/gnuradio/gr-itais/python/messages.py"
    "/home/gnuradio/gr-itais/python/sub_gps.py"
    "/home/gnuradio/gr-itais/python/transmitter.py"
    "/home/gnuradio/gr-itais/python/potumbral.py"
    "/home/gnuradio/gr-itais/python/gmsk_sync.py"
    "/home/gnuradio/gr-itais/python/radio.py"
    "/home/gnuradio/gr-itais/python/rf.py"
    "/home/gnuradio/gr-itais/python/ais_demod.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/itais" TYPE FILE FILES
    "/home/gnuradio/gr-itais/build/python/__init__.pyc"
    "/home/gnuradio/gr-itais/build/python/messages.pyc"
    "/home/gnuradio/gr-itais/build/python/sub_gps.pyc"
    "/home/gnuradio/gr-itais/build/python/transmitter.pyc"
    "/home/gnuradio/gr-itais/build/python/potumbral.pyc"
    "/home/gnuradio/gr-itais/build/python/gmsk_sync.pyc"
    "/home/gnuradio/gr-itais/build/python/radio.pyc"
    "/home/gnuradio/gr-itais/build/python/rf.pyc"
    "/home/gnuradio/gr-itais/build/python/ais_demod.pyc"
    "/home/gnuradio/gr-itais/build/python/__init__.pyo"
    "/home/gnuradio/gr-itais/build/python/messages.pyo"
    "/home/gnuradio/gr-itais/build/python/sub_gps.pyo"
    "/home/gnuradio/gr-itais/build/python/transmitter.pyo"
    "/home/gnuradio/gr-itais/build/python/potumbral.pyo"
    "/home/gnuradio/gr-itais/build/python/gmsk_sync.pyo"
    "/home/gnuradio/gr-itais/build/python/radio.pyo"
    "/home/gnuradio/gr-itais/build/python/rf.pyo"
    "/home/gnuradio/gr-itais/build/python/ais_demod.pyo"
    )
endif()

