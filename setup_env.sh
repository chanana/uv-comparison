#!/bin/bash

echo "===== setting up python venv ====="
python3 -m venv .venv

echo " ===== activating venv ====="
source .venv/bin/activate

echo " ===== installing requirements ====="
pip install --upgrade pip wheel \
            black flake8 \ # formatting tools
            dash_bootstrap_components \
            plotly numpy pandas # install packages

echo " ===== environment setup complete ====="
