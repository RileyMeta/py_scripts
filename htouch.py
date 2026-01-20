# -*- coding: utf-8 -*-
"""
Htouch
==============

Generate a templated C Header file.

Create a C Header file with the basic ifndef and define flags set based on the names provided.

Author: Riley Ava
Created: 20-01-2026
Last Modified: 20-01-2026
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/py_scripts

Requirements:
    - Python 3.10 (or newer)

Usage:
    htouch [option] FILE...

Copyright (c) 2026 Riley Ava
"""
import os, sys
import getopt
from backend import FileMaker, Config

def usage():
    print("Usage: htouch [option] FILE...")

def help_menu():
    usage()
    print("""Generated a templated C Header file

  -v, --verbose   Print more for debugging

  -h, --help      display this help menu and exit
  -V, --version   display version information and exit

Report bugs to: <https://github.com/RileyMeta/py_scripts/pulls>""")

def version_menu():
    print(f"""htouch (Header Touch) 1.0.0
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

    extension: str = ".h"
    FM = FileMaker("htouch", extension)

    for arg in args:
        if arg.endswith(extension):
            arg = arg.replace(extension, "")

        name: str = arg.upper()
        FM.file_template = f"""#ifndef {name}_H
#define {name}_H

#endif
"""
        FM.create_file(arg)

    FM.finish()
