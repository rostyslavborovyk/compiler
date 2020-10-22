#!/bin/bash

python -m pytest

python3 main.py
cd build && make && ./main
