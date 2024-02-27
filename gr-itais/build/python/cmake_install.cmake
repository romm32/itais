# Install script for directory: /home/ais/itais/gr-itais/python

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

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/itais" TYPE FILE FILES
    "/home/ais/itais/gr-itais/python/__init__.py"
    "/home/ais/itais/gr-itais/python/messages.py"
    "/home/ais/itais/gr-itais/python/sub_gps.py"
    "/home/ais/itais/gr-itais/python/transmitter.py"
    "/home/ais/itais/gr-itais/python/potumbral.py"
    "/home/ais/itais/gr-itais/python/gmsk_sync.py"
    "/home/ais/itais/gr-itais/python/radio.py"
    "/home/ais/itais/gr-itais/python/ais_demod.py"
    "/home/ais/itais/gr-itais/python/rf.py"
    "/home/ais/itais/gr-itais/python/itais_radio.py"
    "/home/ais/itais/gr-itais/python/selector_itais.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/itais" TYPE FILE FILES
    "/home/ais/itais/gr-itais/build/python/__init__.pyc"
    "/home/ais/itais/gr-itais/build/python/messages.pyc"
    "/home/ais/itais/gr-itais/build/python/sub_gps.pyc"
    "/home/ais/itais/gr-itais/build/python/transmitter.pyc"
    "/home/ais/itais/gr-itais/build/python/potumbral.pyc"
    "/home/ais/itais/gr-itais/build/python/gmsk_sync.pyc"
    "/home/ais/itais/gr-itais/build/python/radio.pyc"
    "/home/ais/itais/gr-itais/build/python/ais_demod.pyc"
    "/home/ais/itais/gr-itais/build/python/rf.pyc"
    "/home/ais/itais/gr-itais/build/python/itais_radio.pyc"
    "/home/ais/itais/gr-itais/build/python/selector_itais.pyc"
    "/home/ais/itais/gr-itais/build/python/__init__.pyo"
    "/home/ais/itais/gr-itais/build/python/messages.pyo"
    "/home/ais/itais/gr-itais/build/python/sub_gps.pyo"
    "/home/ais/itais/gr-itais/build/python/transmitter.pyo"
    "/home/ais/itais/gr-itais/build/python/potumbral.pyo"
    "/home/ais/itais/gr-itais/build/python/gmsk_sync.pyo"
    "/home/ais/itais/gr-itais/build/python/radio.pyo"
    "/home/ais/itais/gr-itais/build/python/ais_demod.pyo"
    "/home/ais/itais/gr-itais/build/python/rf.pyo"
    "/home/ais/itais/gr-itais/build/python/itais_radio.pyo"
    "/home/ais/itais/gr-itais/build/python/selector_itais.pyo"
    )
endif()

