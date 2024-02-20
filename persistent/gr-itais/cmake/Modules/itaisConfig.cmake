INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ITAIS itais)

FIND_PATH(
    ITAIS_INCLUDE_DIRS
    NAMES itais/api.h
    HINTS $ENV{ITAIS_DIR}/include
        ${PC_ITAIS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ITAIS_LIBRARIES
    NAMES gnuradio-itais
    HINTS $ENV{ITAIS_DIR}/lib
        ${PC_ITAIS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/itaisTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ITAIS DEFAULT_MSG ITAIS_LIBRARIES ITAIS_INCLUDE_DIRS)
MARK_AS_ADVANCED(ITAIS_LIBRARIES ITAIS_INCLUDE_DIRS)
