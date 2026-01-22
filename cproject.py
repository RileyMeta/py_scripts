# -*- coding: utf-8 -*-
"""
cproject
==============

Create a templated C project folder.

Create a C project folder with a src, lib and include folder, a main.c and a Makefile.

Author: Riley Ava
Created: 21/01/2026
Last Modified: 21/01/2026
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/py_scripts

Requirements:
    - Python 3.10 (or newer)

Usage:
    cproject [option] FILE...

Copyright (c) 2026 Riley Ava
"""
import getopt
import os, sys
import subprocess
from pathlib import Path
from getpass import getpass

class Cproject:
    def __init__(self):
        self.projects: list = []
        self.FAILURES: list = []
        self.SUCCESSES: list = []

    def create_projects(self):
        for project in self.projects:
            project_dir = Path(project)

            # If the directory already exists
            if project_dir.is_dir():
                if self.confirm_overwrite(project):
                    self.clean(project)
                else:
                    self.FAILURES.append(project)
                    continue # skip to the next item

            sub_directories = (project,
                            f"{project}/lib",
                            f"{project}/include",
                            f"{project}/src")

            for sub_dir in sub_directories:
                self.create_folder(sub_dir)

            self.create_readme(project)
            self.create_mainsrc(project)
            self.create_makefile(project)

    def confirm_overwrite(self, name: str) -> bool:
        prompt: str = f"{name} already exists.\n"
        prompt += "Would you like to overwrite it?\n"
        prompt += "[NOTE!] This will delete the folder and it's contents."

        try:
            while True:
                print(prompt)
                response = input("[Y]es or [N]o: ").lower()
                if response in ("y", "yes"):
                    return True
                elif response in ("n", "no"):
                    return False
                else:
                    print(f"{response} is not recognized.")
                    getpass("Press [enter] to continue")
                    continue
        except KeyboardInterrupt:
            print("\nOperation was cancelled.")
            sys.exit(-1)

    def clean(self, name: str):
        command: list = ["rm", "-rf", name]
        subprocess.run(command)

    def create_folder(self, name: str):
        command: list = ["mkdir", "-pv", name]
        subprocess.run(command)

    def create_makefile(self, name: str):
        command: list = ["makefile", name]
        subprocess.run(command)

    def create_mainsrc(self, name: str):
        command: list = ["ctouch", f"{name}/src/main.c"]
        subprocess.run(command)

    def create_readme(self, name: str):
        try:
            readme: str = f"{name}/README.md"
            with open(readme, 'w') as f:
                if "/" in name:
                    pieces = name.split("/")
                    name = pieces[len(pieces) - 1]
                f.write(f"# {name}")
            print("readme: 1 file(s) created.")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

def usage():
    print("Usage: cproject [option] FILE...")

def help_menu():
    usage()
    print("""Generated a templated C project folder

  -v, --verbose   Print more for debugging

  -h, --help      display this help menu and exit
  -V, --version   display version information and exit

Report bugs to: <https://github.com/RileyMeta/py_scripts/pulls>""")

def version_menu():
    print(f"""cproject (C Project) 1.0.0
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

    C = Cproject()
    for arg in args:
        C.projects.append(arg)

    C.create_projects()