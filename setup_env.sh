#!/bin/bash

echo "setting up python venv"
echo "python3 -m venv .venv"
python3 -m venv .venv

echo "activating venv"
echo "source .venv/bin/activate"
source .venv/bin/activate

echo "installing requirements"
echo "pip install --upgrade pip wheel"
pip install --upgrade pip wheel

echo "pip intall -r requirements.txt"
pip install -r requirements.txt

echo "environment setup complete"
