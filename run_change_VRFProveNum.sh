#!/bin/bash

# Delete previous output files
rm -f VRFProveNum_time_*.txt

# Run choose_satellite_gateway.py 1000 times for each input from 1 to 10
for i in {1..10}  # Number of VRFprove
do
  for j in {1..1000}  # Repeat 1000 times
  do
    echo "Running with number_of_VRFprove=$i, iteration=$j"
    python change_VRFProveNum.py $i
  done
done
