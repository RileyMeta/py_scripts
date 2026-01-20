# PyScripts
These are all scripts that mimic the touch function in unix, but also create a templated file based on the type.

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
### Makefile
