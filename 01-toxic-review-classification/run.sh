#!/bin/bash

# Prepare dataset
python3 main.py prepare-data -i prepared-dataset/code-review-dataset-full.xlsx \
    -o processed-dataset

# Run classifiers
python3 main.py classify
