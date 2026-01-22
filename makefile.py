# -*- coding: utf-8 -*-
"""
Makefile
==============

Brief description of the program.

Full description of the program with technical information about the process.

Author: Riley Ava
Created: 20-01-2026
Last Modified: 21-01-2026
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/py_scripts

Requirements:
    - Python 3.10 (or newer)

Usage:
    makefile [option] FILE...

Copyright (c) 2026 Riley Ava
"""
import os, sys
import getopt
from backend import FileMaker, Config

def usage():
    print("Usage: makefile [option] FILE...")

def help_menu():
    usage()
    print("""Generated a templated Makefile

  -v, --verbose   Print more for debugging

  -h, --help      display this help menu and exit
  -V, --version   display version information and exit

Report bugs to: <https://github.com/RileyMeta/py_scripts/pulls>""")

def version_menu():
    print(f"""makefile (makefile Touch) 1.0.0
Copyright (C) 2026 Riley Ava.
License MPL2.0: Mozilla Public License 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Riley Ava.""")

if __name__ == "__main__":
    short_opts = "Vv"
    long_opts = ["help", "version", "verbose"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("--help"):
            help_menu()
            sys.exit(0)
        elif opt in ("-V", "--version"):
            version_menu()
            sys.exit(0)
        elif opt in ("-v", "--verbose"):
            Config.VERBOSE = True

    if not args:
        usage()
        sys.exit(1)

    FM = FileMaker("makefile", "")
    for arg in args:
        name: str = arg
        if "/" in name:
            pieces = name.split("/")
            name = pieces[len(pieces) - 1]

        FM.file_template = f"""TARGET = {name}
SRC := $(wildcard src/*.c)

# Compiler and Flags
CC = gcc
CFLAGS = -Wall -std=c99 -Wno-missing-braces -Iinclude

# Libraries and linking
# LIBS = -lraylib -lGL -lm -lpthread -ldl -lrt -lX11

# Build rule
$(TARGET): $(SRC)
	$(CC) $(SRC) -o $(TARGET) $(CFLAGS) $(LIBS)

# Clean rule
clean:
	rm -f $(TARGET)

# Run rule
run: $(TARGET)
	./$(TARGET)
"""
        FM.create_file("Makefile")

    FM.finish()
