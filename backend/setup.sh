#!/bin/bash
# Setup script for Swach AI Carbon Agent Backend
# Run this to install dependencies and verify setup

set -e

echo "============================================"
echo "Swach AI Carbon Agent - Backend Setup"
echo "============================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "✓ Creating Python virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo ""
echo "✓ Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

echo ""
echo "============================================"
echo "Setup Complete! ✓"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Create .env file:"
echo "   cp .env.example .env"
echo "   # Then add your API keys to .env"
echo ""
echo "2. Run tests to verify calculator:"
echo "   pytest test_calculator.py -v"
echo ""
echo "3. Run a quick test:"
echo "   python -c \"from tools.calculator import *; print('✓ Import successful')\""
echo ""
