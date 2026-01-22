# PyScripts
These are all scripts that mimic the touch function in unix, but also create a templated file based on the type.
# Full Install
Complete script to setup and install at the same time
```sh
mkdir -p ~/.local/bin/ && cd ~/.local/bin/
git clone https://github.com/RileyMeta/py_scripts.git
cd py_scripts
sh setup.sh && sh setup.sh install
```
## Setup
There's a very simple setup script that will create a virtual environment and install the module, allowing you to symlink the files to work like a binary.
```sh
sh setup.sh
```
Simplified (done in the root folder):
```sh
python3 -m venv venv
source venv/bin/activate
pip install ./backend
```
> [!note]
> There is either a bug or some intended behavior I don't know about that prevents these scripts from working if you pass the editable (`-e`) flag.

followed by a check to ensure they all use the same / correct virtual environment 'shebang (`#!`)' when running.
```sh
for prog in "${PROGRAMS[@}"; do
    echo "$shebang" > tmp_file
    cat "$prog" >> tmp_file
    mv tmp_file "$prog"
done
```
## Install
I merged the bash scripts into a single file, they still symlink the python file(s) to your `~/.local/bin/` directory which should allow you to execute the programs as if they were native apps (for your specific user).
```sh
sh setup.sh install
```
> [!NOTE]
> Do not forget, when using `~/.local/bin/` it needs to be added to your `PATH`, the install will check and warn you.
## Types
- Ctouch: Create a generic C templated file
- Htouch: Create a formatted header file
- Pytouch: Create a python file with basic info
- Makefile: Create a Makefile for a C project

## Templates
These are the actual templates that are used for each touch program.
### C
```c
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, World!\n");

    return 0;
}
```
### H
```c
#ifndef FILENAME_H
#define FILENAME_H

#endif
```
### Py
```python
# -*- coding: utf-8 -*-
"""
Filename
==============

Brief desription of the program.

Detailed description of the program explaining simple functions.

Author: Riley Ava
Created: {date}
Last Modified: {date}
Version: 1.0.0
License: MPL 2.0
Repository: https://github.com/RileyMeta/{name}

Requirements:
    - Python 3.10 (or newer)

Usage:
    {name} [option] FILE...

Copyright (c) {year} Riley Ava
"""
```
### Makefile
```make
TARGET = {name}
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
```
