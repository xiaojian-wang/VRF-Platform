from RSA_VRF import *
from argparse import ArgumentParser
import random
import sys
import json
import time



def main():

    # Check if the satellite_number is provided via command line
    if len(sys.argv) != 2:
        print("Usage: python choose_satellite_gateway.py <satellite_number>")
        sys.exit(1)

    # Parse the satellite_number from command line
    try:
        satellite_number = int(sys.argv[1])
    except ValueError:
        print("Error: choose_satellite_gateway must be an integer.")
        sys.exit(1)
    

    VRF_sk, VRF_pk, k = VRF_keygen()
    
    num_of_secrets = 1
    random.seed(1023)
    secret_a0_list = [random.randint(1, 10000000000) for i in range(num_of_secrets)]

    secret_a0 = secret_a0_list[0] # each time consider one secret

    time_VRFProve_start = time.time()
    pi = RSA_FDH_VRF.prove(VRF_sk, str(secret_a0), k)
    y = RSA_FDH_VRF.proof2hash(pi)
    time_VRFProve_end = time.time()
    VRF_prove_time_file_name = "VRF_prove_time_{}.txt".format(satellite_number)
    with open(VRF_prove_time_file_name, 'a') as f:
        f.write(str(time_VRFProve_end - time_VRFProve_start))
        f.write('\n')

    # choose the closest satellite 
    closest_satellite = None
    min_difference = float('inf')
    # first read the satellite name from the file
    with open(f"satellite_ports_{satellite_number}.json", 'r') as f:
        satellite_ports = json.load(f)
    # Iterate over the satellite names and ports
    time_choose_satellite_start = time.time()
    for satellite_name, port in satellite_ports.items():
        # Hash the satellite name (to ensure it's comparable to y)
        satellite_hash = int(hashlib.sha256(satellite_name.encode()).hexdigest(), 16)
        # print("type of y: ", type(y))

        # satellite_hash = hashlib.sha256(satellite_name.encode()).hexdigest()
        # print("type of satellite_hash: ", type(satellite_hash))
        # satellite_hash to bytes
        # satellite_hash = bytes.fromhex(satellite_hash)
        y_int = int.from_bytes(y, byteorder='big')
        satellite_hash_int = int(satellite_hash)

        # Calculate the difference between y and the satellite hash
        difference = abs(satellite_hash_int - y_int)
        
        # Find the satellite with the smallest difference
        if difference < min_difference:
            min_difference = difference
            closest_satellite = satellite_name
    time_choose_satellite_end = time.time()
    choose_satellite_time_file_name = "choose_satellite_time_{}.txt".format(satellite_number)
    with open(choose_satellite_time_file_name, 'a') as f:
        f.write(str(time_choose_satellite_end - time_choose_satellite_start))
        f.write('\n')
    print("The closest satellite is: ", closest_satellite) 


    # verify the VRF proof
    time_check_proof_start = time.time()
    VRF_is_valid = RSA_FDH_VRF.verifying(VRF_pk, str(secret_a0), pi, k)
    time_check_proof_end = time.time()
    check_proof_time_file_name = "check_proof_time_{}.txt".format(satellite_number)
    with open(check_proof_time_file_name, 'a') as f:
        f.write(str(time_check_proof_end - time_check_proof_start))
        f.write('\n')
    print("valid VRF proof: ", VRF_is_valid)


if __name__ == '__main__':
    main()