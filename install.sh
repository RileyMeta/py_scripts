#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
RESET='\033[0m' # No Color

# Get the absolute path to the root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure ~/.local/bin exists
mkdir -p ~/.local/bin

echo -e "${BLUE}Installing programs to ~/.local/bin...${RESET}"

# List of programs to install (add/remove as needed)
PROGRAMS=("ctouch.py" "htouch.py" "makefile.py" "pytouch.py")

for prog in "${PROGRAMS[@]}"; do
    if [ -f "$ROOT_DIR/$prog" ]; then
        # Make the original file executable
        chmod +x "$ROOT_DIR/$prog"

        # Create symlink name (remove .py extension)
        link_name=$(basename "$prog" .py)

        # Remove existing symlink if it exists
        rm -f ~/.local/bin/$link_name

        # Create symlink
        ln -s "$ROOT_DIR/$prog" ~/.local/bin/$link_name

        echo -e "${GREEN}✓ Installed $link_name${RESET}"
    else
        echo -e "${RED}✗ $prog not found${RESET}"
    fi
done

echo -e "${BLUE}Installation complete!${RESET}"
echo -e "${BLUE}Make sure ~/.local/bin is in your PATH${RESET}"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${RED}⚠ ~/.local/bin is not in your PATH${RESET}"
    echo -e "${BLUE}Add this to your ~/.bashrc or ~/.zshrc:${RESET}"
    echo -e "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
