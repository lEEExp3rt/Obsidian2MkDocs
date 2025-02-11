#!/usr/bin/bash

rm -rf output
find . -name "__pycache__" -type d | xargs rm -rf