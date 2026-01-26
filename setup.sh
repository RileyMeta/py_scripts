#!/bin/bash

set -euo pipefail

# Colors for output
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
RESET='\033[0m' # No Color

# Folders ends with no slash to make it easier to combine for later steps
# Array of programs managed by this script
PROGRAMS=("cproject.py" "ctouch.py" "htouch.py" "makefile.py" "pytouch.py" "random_meme.py")
USER="$(whoami)"
INSTALL_DIR=".local/bin"
SHEBANG='#!/home'
SHEBANG=$SHEBANG"/$USER/$INSTALL_DIR/py_scripts/venv/bin/python3"

delete_venv() {
    venv="/home/$USER/$INSTALL_DIR/py_scripts/venv/"
    echo -e "  ${YELLOW}ˣPurging: $venv${RESET}"
    rm -rf "$venv"
}

init_venv() {
    echo -e "${BLUE}Setting up virtual environment...${RESET}"

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${RESET}"
    else
        echo -e "${GREEN}✓ Virtual environment already exists${RESET}"
    fi

    # Check if the venv has the pip package 'backend' installed
    command="${SHEBANG#??}"
    if ! $command -m pip list | grep -q backend; then
        # Activate virtual environment
        source venv/bin/activate

        echo -e "${BLUE}Installing backend module...${RESET}"

        # Install the backend module in editable mode
        pip install ./backend
    fi

    echo -e "${GREEN}✓ Setup complete!${RESET}"
    echo -e "${BLUE}To activate the virtual environment, run:${RESET}"
    echo -e "  source venv/bin/activate"
}

fix_venv_path() {
    for prog in "${PROGRAMS[@]}"; do
        if ! grep -q "$SHEBANG" "$prog"; then
            echo "$SHEBANG" > temp_file
            cat "$prog" >> temp_file
            mv temp_file "$prog"
        fi
    done

    echo -e "${GREEN}✓ Shebangs updated!${RESET}"
}

fix_delete_autocomplete() {
    local rc="$HOME/.bashrc"

    while [ true ]; do
        if ! grep -q "_delete_complete()" "$rc"; then
            echo -e "${RED}Delete auto-complete function is not found${RESET}"
            cat <<"EOF" >> ~/.bashrc

_delete_complete() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local trash_dir="$HOME/.local/share/Trash/files"

    # If the previous word was 'restore', complete with trash filenames
    if [[ "$prev" == "restore" ]] || [[ "$prev" == "-r" ]]; then
        if [[ -d "$trash_dir" ]]; then
            COMPREPLY=( $(cd "$trash_dir" && compgen -f -- "$cur") )
        fi
    fi
}

complete -F _delete_complete delete
EOF
            echo -e "  ${YELLOW}Function added to $rc${RESET}"
            continue
        else
            echo -e "${GREEN}Delete auto-complete function was found${RESET}"
            source "$rc"
            break
        fi
    done
}

install() {
    # Get the absolute path to the root directory
    ROOT_DIR="/home/$(whoami)"
    SETUP_DIR="$ROOT_DIR/.local/bin/py_scripts"

    # Ensure ~/.local/bin exists
    mkdir -p "$ROOT_DIR/.local/bin"

    echo -e "${BLUE}Installing programs to ~/.local/bin...${RESET}"

    for prog in "${PROGRAMS[@]}"; do
        # Make the original file executable
        chmod +x "$SETUP_DIR/$prog"

        if [ -f "$SETUP_DIR/$prog" ]; then
            # Create symlink name (remove .py extension)
            link_name=$(basename "$prog" .py)
            echo "$link_name"

            # Remove existing symlink if it exists
            rm -f "$ROOT_DIR/.local/bin/$link_name"

            # Create symlink
            ln -s "$SETUP_DIR/$prog" "$ROOT_DIR/.local/bin/$link_name"
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
      clean      delete the virtual environment and create a new one

      --help     display this help information and exit
      --version  display version information and exit

Report bugs to: <https://github.com/RileyMeta/py_scripts/pulls>
Py_sctips home page: <https://github.com/RileyMeta/py_scripts>
EOF
}

version_menu() {
    cat <<EOF
py_scripts setup script 1.1.0
Copyright (C) 2026 Riley Ava.
License MPL2.0: Mozilla Public License 2.0 <https://www.mozilla.org/en-US/MPL/2.0/>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Riley Ava.
EOF
}


main() {
    declare -a argv=("$@")
    local argc="${#argv[@]}"

    for ((i=0; i<argc; i++)); do
        local arg="${argv[i]}"

        case "$arg" in
            "--help")
                help_menu
                return 0 ;;
            "--version"|"-v")
                version_menu
                return 0 ;;
            "install")
                install 
                return 0 ;;
            "clean")
                delete_venv ;;
            *)
                usage
                return 1 ;;
        esac
    done

    init_venv
    fix_venv_path
    fix_delete_autocomplete
    return 0
}

main "$@"
