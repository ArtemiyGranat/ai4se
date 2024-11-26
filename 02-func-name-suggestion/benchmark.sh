#!/bin/bash

echo "Preparing data for Python"
python3 main.py prepare-data -u code_search_net -l python -o prepared-dataset-python

echo "Preparing data for Ruby"
python3 main.py prepare-data -u code_search_net -l ruby -o prepared-dataset-ruby

echo "Getting results for Python without comments"
python3 main.py predict-names -d prepared-dataset-python -m Salesforce/codet5p-220m

echo "Getting results for Python with comments"
python3 main.py predict-names -d prepared-dataset-python -m Salesforce/codet5p-220m -c

echo "Getting results for Ruby without comments"
python3 main.py predict-names -d prepared-dataset-ruby -m Salesforce/codet5p-220m

echo "Getting results for Ruby with comments"
python3 main.py predict-names -d prepared-dataset-ruby -m Salesforce/codet5p-220m -c

