#!/bin/bash

python main.py
cd tests && make && ./test_1
