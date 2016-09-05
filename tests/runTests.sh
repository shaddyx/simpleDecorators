#!/bin/sh
export PYTHONPATH=$PYTHONPATH:../
python -m unittest discover -p "*Test.py"
