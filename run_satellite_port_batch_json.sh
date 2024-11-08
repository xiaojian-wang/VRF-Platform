#!/bin/bash

# Check if Python script exists
if [ ! -f satellite_port_batch_json.py ]; then
    echo "Error: satellite_port_batch_json.py not found."
    exit 1
fi

# Generate JSON files for satellite_number from 10 to 50
for i in {10..50..10}; do
    python3 satellite_port_batch_json.py "$i"
done

echo "All JSON files generated successfully for satellite numbers 10 to 50."
