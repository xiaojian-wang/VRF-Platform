#!/bin/bash

for i in {10..50..10}; do
    VRF_prove_time_file="VRF_prove_time_$i.txt"
    choose_satellite_time_file="choose_satellite_time_$i.txt"
    check_proof_time_file="check_proof_time_$i.txt"
    
    if [ -f "$VRF_prove_time_file" ]; then
        echo "Deleting existing $VRF_prove_time_file"
        rm -f "$VRF_prove_time_file"
    fi

    if [ -f "$choose_satellite_time_file" ]; then
        echo "Deleting existing $choose_satellite_time_file"
        rm -f "$choose_satellite_time_file"
    fi
    
    if [ -f "$check_proof_time_file" ]; then
        echo "Deleting existing $check_proof_time_file"
        rm -f "$check_proof_time_file"
    fi
    
    echo "Running python choose_satellite_gateway.py $i 1000 times"
    for ((j=1; j<=1000; j++)); do
        python3 choose_satellite_gateway.py $i
    done
done
