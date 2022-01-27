#!/bin/bash
echo ================ Estimating the number of family farmers by state ... ================


printf "=== Downloading pandas python library ===\n"
pip3 install pandas
printf "=== Finished downloading pandas python library ===\n"

printf "=== Downloading numpy python library ===\n"
pip3 install numpy
printf "=== Finished downloading numpy python library ===\n"

printf "=== Running compute_ranchers.py script ===\n"
python3 compute_ranchers.py
printf "=== Finished running compute_ranchers.py script ===\n"

echo ================ Finished estimating the number of family farmers by state ... ================