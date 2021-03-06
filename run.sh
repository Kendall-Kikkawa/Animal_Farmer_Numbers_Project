#!/bin/bash
echo ================ Estimating the number of family farmers by state ... ================


printf "\n=== Downloading pandas python library ===\n"
pip3 install pandas
printf "\n=== Finished downloading pandas python library ===\n"

printf "\n=== Downloading numpy python library ===\n"
pip3 install numpy
printf "\n=== Finished downloading numpy python library ===\n"

printf "\n=== Downloading openpyxl python library ===\n"
pip3 install openpyxl
printf "\n=== Finished downloading openpyxl python library ===\n"

printf "\n=== Running compute_animal_farmers.py script ===\n"
python3 compute_animal_farmers.py
printf "\n=== Finished running compute_animal_farmers.py script ===\n\n"

echo ================ Finished estimating the number of family farmers by state ... ================