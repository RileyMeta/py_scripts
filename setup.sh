#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up virtual environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

echo -e "${BLUE}Installing backend module...${NC}"

# Install the backend module in editable mode
pip install ./backend

echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${BLUE}To activate the virtual environment, run:${NC}"
echo -e "  source venv/bin/activate"
