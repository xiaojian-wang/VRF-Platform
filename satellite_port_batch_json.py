import json
import sys

# Check if the satellite_number is provided via command line
if len(sys.argv) != 2:
    print("Usage: python generate_satellite_ports.py <satellite_number>")
    sys.exit(1)

# Parse the satellite_number from command line
try:
    satellite_number = int(sys.argv[1])
except ValueError:
    print("Error: satellite_number must be an integer.")
    sys.exit(1)

# Create a dictionary with keys 'satellite_1' to 'satellite_n'
satellite_ports = {f"satellite_{i}": 50140 + i for i in range(satellite_number)}

# Write the data to a JSON file
output_filename = f"satellite_ports_{satellite_number}.json"
with open(output_filename, "w") as file:
    json.dump(satellite_ports, file, indent=4)

print(f"JSON file '{output_filename}' generated successfully.")
