# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/gnuradio/gr-itais

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/gnuradio/gr-itais/build

# Include any dependencies generated for this target.
include swig/CMakeFiles/itais_swig.dir/depend.make

# Include the progress variables for this target.
include swig/CMakeFiles/itais_swig.dir/progress.make

# Include the compile flags for this target's objects.
include swig/CMakeFiles/itais_swig.dir/flags.make

swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o: swig/CMakeFiles/itais_swig.dir/flags.make
swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o: swig/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/gnuradio/gr-itais/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o"
	cd /home/gnuradio/gr-itais/build/swig && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o -c /home/gnuradio/gr-itais/build/swig/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx

swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.i"
	cd /home/gnuradio/gr-itais/build/swig && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/gnuradio/gr-itais/build/swig/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx > CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.i

swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.s"
	cd /home/gnuradio/gr-itais/build/swig && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/gnuradio/gr-itais/build/swig/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx -o CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.s

# Object files for target itais_swig
itais_swig_OBJECTS = \
"CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o"

# External object files for target itais_swig
itais_swig_EXTERNAL_OBJECTS =

swig/_itais_swig.so: swig/CMakeFiles/itais_swig.dir/CMakeFiles/itais_swig.dir/itais_swigPYTHON_wrap.cxx.o
swig/_itais_swig.so: swig/CMakeFiles/itais_swig.dir/build.make
swig/_itais_swig.so: lib/libgnuradio-itais.so.1.0.0.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libpython3.8.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgnuradio-filter.so.3.8.5.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgnuradio-fft.so.3.8.5.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libfftw3f.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libfftw3f_threads.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgnuradio-blocks.so.3.8.5.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgnuradio-runtime.so.3.8.5.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libthrift.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgnuradio-pmt.so.3.8.5.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_program_options.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_regex.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libboost_atomic.so.1.71.0
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/liblog4cpp.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgmpxx.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libgmp.so
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/libvolk.so.2.2
swig/_itais_swig.so: /usr/lib/x86_64-linux-gnu/liborc-0.4.so
swig/_itais_swig.so: swig/CMakeFiles/itais_swig.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/gnuradio/gr-itais/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module _itais_swig.so"
	cd /home/gnuradio/gr-itais/build/swig && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/itais_swig.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
swig/CMakeFiles/itais_swig.dir/build: swig/_itais_swig.so

.PHONY : swig/CMakeFiles/itais_swig.dir/build

swig/CMakeFiles/itais_swig.dir/clean:
	cd /home/gnuradio/gr-itais/build/swig && $(CMAKE_COMMAND) -P CMakeFiles/itais_swig.dir/cmake_clean.cmake
.PHONY : swig/CMakeFiles/itais_swig.dir/clean

swig/CMakeFiles/itais_swig.dir/depend:
	cd /home/gnuradio/gr-itais/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gnuradio/gr-itais /home/gnuradio/gr-itais/swig /home/gnuradio/gr-itais/build /home/gnuradio/gr-itais/build/swig /home/gnuradio/gr-itais/build/swig/CMakeFiles/itais_swig.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : swig/CMakeFiles/itais_swig.dir/depend

