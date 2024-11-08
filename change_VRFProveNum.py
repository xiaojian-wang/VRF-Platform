from RSA_VRF import *
from argparse import ArgumentParser
import random
import sys
import json
import time
import hashlib


def main():

    # Check if the number_of_VRFprove is provided via command line
    if len(sys.argv) != 2:
        print("Usage: python choose_satellite_gateway.py <number_of_VRFprove>")
        sys.exit(1)

    # Parse the number_of_VRFprove from command line
    try:
        number_of_VRFprove = int(sys.argv[1])
    except ValueError:
        print("Error: number_of_VRFprove must be an integer.")
        sys.exit(1)

    VRF_sk, VRF_pk, k = VRF_keygen()

    random.seed(1023)
    secrets = [random.randint(1, 10000000000) for _ in range(number_of_VRFprove)]
    
    
    VRFProveNum_time_file_name = f"VRFProveNum_time_{number_of_VRFprove}.txt"

    time_VRFProve_start = time.time()
    for secret_a0 in secrets:
        pi = RSA_FDH_VRF.prove(VRF_sk, str(secret_a0), k)
        y = RSA_FDH_VRF.proof2hash(pi)
    time_VRFProve_end = time.time()

    with open(VRFProveNum_time_file_name, 'a') as f:
        f.write(str(time_VRFProve_end - time_VRFProve_start))
        f.write('\n')

    # choose the closest satellite (example with satellite_number=1 for simplicity)
    satellite_number = 30
    closest_satellite = None
    min_difference = float('inf')

    with open(f"satellite_ports_{satellite_number}.json", 'r') as sf:
        satellite_ports = json.load(sf)

    # time_choose_satellite_start = time.time()
    for satellite_name, port in satellite_ports.items():
        satellite_hash = int(hashlib.sha256(satellite_name.encode()).hexdigest(), 16)
        y_int = int.from_bytes(y, byteorder='big')
        satellite_hash_int = int(satellite_hash)
        difference = abs(satellite_hash_int - y_int)

        if difference < min_difference:
            min_difference = difference
            closest_satellite = satellite_name
    # time_choose_satellite_end = time.time()

    print("The closest satellite is:", closest_satellite)

    # time_check_proof_start = time.time()
    VRF_is_valid = RSA_FDH_VRF.verifying(VRF_pk, str(secret_a0), pi, k)
    # time_check_proof_end = time.time()
    print("valid VRF proof:", VRF_is_valid)


if __name__ == '__main__':
    main()
