INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FOSDEM fosdem)

FIND_PATH(
    FOSDEM_INCLUDE_DIRS
    NAMES fosdem/api.h
    HINTS $ENV{FOSDEM_DIR}/include
        ${PC_FOSDEM_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FOSDEM_LIBRARIES
    NAMES gnuradio-fosdem
    HINTS $ENV{FOSDEM_DIR}/lib
        ${PC_FOSDEM_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FOSDEM DEFAULT_MSG FOSDEM_LIBRARIES FOSDEM_INCLUDE_DIRS)
MARK_AS_ADVANCED(FOSDEM_LIBRARIES FOSDEM_INCLUDE_DIRS)

