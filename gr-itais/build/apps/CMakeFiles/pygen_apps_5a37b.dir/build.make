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

# Utility rule file for pygen_apps_5a37b.

# Include the progress variables for this target.
include apps/CMakeFiles/pygen_apps_5a37b.dir/progress.make

apps/CMakeFiles/pygen_apps_5a37b: apps/ais_rx.exe
apps/CMakeFiles/pygen_apps_5a37b: apps/ais_tx.exe
apps/CMakeFiles/pygen_apps_5a37b: apps/itais_tx.exe


apps/ais_rx.exe: ../apps/ais_rx
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/gnuradio/gr-itais/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Shebangin ais_rx"
	cd /home/gnuradio/gr-itais/build/apps && /usr/bin/python3 -c "import re; R=re.compile('^#!.*\$$\\n',flags=re.MULTILINE); open('/home/gnuradio/gr-itais/build/apps/ais_rx.exe','w').write('#!/usr/bin/python3\\n'+R.sub('',open('/home/gnuradio/gr-itais/apps/ais_rx','r').read()))"

apps/ais_tx.exe: ../apps/ais_tx
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/gnuradio/gr-itais/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Shebangin ais_tx"
	cd /home/gnuradio/gr-itais/build/apps && /usr/bin/python3 -c "import re; R=re.compile('^#!.*\$$\\n',flags=re.MULTILINE); open('/home/gnuradio/gr-itais/build/apps/ais_tx.exe','w').write('#!/usr/bin/python3\\n'+R.sub('',open('/home/gnuradio/gr-itais/apps/ais_tx','r').read()))"

apps/itais_tx.exe: ../apps/itais_tx
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/gnuradio/gr-itais/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Shebangin itais_tx"
	cd /home/gnuradio/gr-itais/build/apps && /usr/bin/python3 -c "import re; R=re.compile('^#!.*\$$\\n',flags=re.MULTILINE); open('/home/gnuradio/gr-itais/build/apps/itais_tx.exe','w').write('#!/usr/bin/python3\\n'+R.sub('',open('/home/gnuradio/gr-itais/apps/itais_tx','r').read()))"

pygen_apps_5a37b: apps/CMakeFiles/pygen_apps_5a37b
pygen_apps_5a37b: apps/ais_rx.exe
pygen_apps_5a37b: apps/ais_tx.exe
pygen_apps_5a37b: apps/itais_tx.exe
pygen_apps_5a37b: apps/CMakeFiles/pygen_apps_5a37b.dir/build.make

.PHONY : pygen_apps_5a37b

# Rule to build all files generated by this target.
apps/CMakeFiles/pygen_apps_5a37b.dir/build: pygen_apps_5a37b

.PHONY : apps/CMakeFiles/pygen_apps_5a37b.dir/build

apps/CMakeFiles/pygen_apps_5a37b.dir/clean:
	cd /home/gnuradio/gr-itais/build/apps && $(CMAKE_COMMAND) -P CMakeFiles/pygen_apps_5a37b.dir/cmake_clean.cmake
.PHONY : apps/CMakeFiles/pygen_apps_5a37b.dir/clean

apps/CMakeFiles/pygen_apps_5a37b.dir/depend:
	cd /home/gnuradio/gr-itais/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gnuradio/gr-itais /home/gnuradio/gr-itais/apps /home/gnuradio/gr-itais/build /home/gnuradio/gr-itais/build/apps /home/gnuradio/gr-itais/build/apps/CMakeFiles/pygen_apps_5a37b.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : apps/CMakeFiles/pygen_apps_5a37b.dir/depend

