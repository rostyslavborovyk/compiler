#!/bin/bash

python3 compiler.py
cd build && make && ./main
