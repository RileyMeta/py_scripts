#!/bin/bash

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
RESET='\033[0m' # No Color

# Array of programs managed by this script
PROGRAMS=("ctouch.py" "htouch.py" "makefile.py" "pytouch.py")

init_venv() {
    echo -e "${BLUE}Setting up virtual environment...${RESET}"

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${RESET}"
    else
        echo -e "${GREEN}✓ Virtual environment already exists${RESET}"
    fi

    # Activate virtual environment
    source venv/bin/activate

    echo -e "${BLUE}Installing backend module...${RESET}"

    # Install the backend module in editable mode
    pip install ./backend

    echo -e "${GREEN}✓ Setup complete!${RESET}"
    echo -e "${BLUE}To activate the virtual environment, run:${RESET}"
    echo -e "  source venv/bin/activate"

    fix_venv_path
}

fix_venv_path() {
    shebang='#!/home/'
    shebang=$shebang"$(whoami)/.local/bin/py_scripts/venv/bin/python3"

    for prog in "${PROGRAMS[@]}"; do
        if ! grep -q "$shebang" "$prog"; then
            echo "$shebang" > temp_file
            cat "$prog" >> temp_file
            mv temp_file "$prog"
        fi
    done

    echo -e "${GREEN}✓ Shebangs updated!${RESET}"
}

install() {
    # Get the absolute path to the root directory
    ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Ensure ~/.local/bin exists
    mkdir -p ~/.local/bin

    echo -e "${BLUE}Installing programs to ~/.local/bin...${RESET}"

    for prog in "${PROGRAMS[@]}"; do
        if [ -f "$ROOT_DIR/$prog" ]; then
            # Make the original file executable
            chmod +x "$ROOT_DIR/$prog"

            # Create symlink name (remove .py extension)
            link_name=$(basename "$prog" .py)

            # Remove existing symlink if it exists
            rm -f ~/.local/bin/"$link_name"

            # Create symlink
            ln -s "$ROOT_DIR/$prog" ~/.local/bin/"$link_name"
            echo -e "${GREEN}✓ Installed $link_name${RESET}"
        else
            echo -e "${RED}✗ $prog not found${RESET}"
        fi
    done

    echo -e "${BLUE}Installation complete!${RESET}"

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${RED}⚠ ~/.local/bin is not in your PATH${RESET}"
        echo -e "${BLUE}Add this to your ~/.bashrc or ~/.zshrc:${RESET}"
        echo -e "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

usage() {
    echo -e "Usage: setup.sh [option]"
}

help_menu() {
    usage
    cat <<EOF
Setup and install the py_scripts as programs.

      install    change permissions and install with symlinks

      --help     display this help information and exit
      --version  display version information and exit

Report bugs to: <https://github.com/RileyMeta/py_scripts/pulls>
Py_sctips home page: <https://github.com/RileyMeta/py_scripts>
EOF
}

version_menu() {
    cat <<EOF
py_scripts setup script 1.0.0
Copyright (C) 2026 Riley Ava.
License MPL2.0: Mozilla Public License 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Riley Ava.
EOF
}


main() {
    declare -a argv="$*"
    argc="${#argv[@]}"

    if [[ ! -z "$argv" ]]; then
        for arg in "${argv[@]}"; do
            if [[ "$arg" == "--help" ]]; then
                help_menu
                return 0
            elif [[ "$arg" == "--version" || "$arg" == "-v" ]]; then
                version_menu
                return 0
            elif [[ "$arg" == "install" ]]; then
                install
                return 0
            else
                echo -e "$arg is not recognized."
                usage
                return 1
            fi
        done
    fi

    init_venv
    return 0
}

main "$@"
