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

# Utility rule file for itais_swig_swig_doc.

# Include the progress variables for this target.
include swig/CMakeFiles/itais_swig_swig_doc.dir/progress.make

swig/CMakeFiles/itais_swig_swig_doc: swig/itais_swig_doc.i


itais_swig_swig_doc: swig/CMakeFiles/itais_swig_swig_doc
itais_swig_swig_doc: swig/CMakeFiles/itais_swig_swig_doc.dir/build.make

.PHONY : itais_swig_swig_doc

# Rule to build all files generated by this target.
swig/CMakeFiles/itais_swig_swig_doc.dir/build: itais_swig_swig_doc

.PHONY : swig/CMakeFiles/itais_swig_swig_doc.dir/build

swig/CMakeFiles/itais_swig_swig_doc.dir/clean:
	cd /home/gnuradio/gr-itais/build/swig && $(CMAKE_COMMAND) -P CMakeFiles/itais_swig_swig_doc.dir/cmake_clean.cmake
.PHONY : swig/CMakeFiles/itais_swig_swig_doc.dir/clean

swig/CMakeFiles/itais_swig_swig_doc.dir/depend:
	cd /home/gnuradio/gr-itais/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gnuradio/gr-itais /home/gnuradio/gr-itais/swig /home/gnuradio/gr-itais/build /home/gnuradio/gr-itais/build/swig /home/gnuradio/gr-itais/build/swig/CMakeFiles/itais_swig_swig_doc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : swig/CMakeFiles/itais_swig_swig_doc.dir/depend

