import sys
import os
import csv
import time

import XORHASH
import SHA



def hash_files(file, hashing_algorithm, salt_set):
    """
    Hashes the given file based on the specified hashing algorithm.

    Args:
        file (str): The path of the file to be hashed.
        hashing_algorithm (str): The hashing algorithm to be used (XOR or SHA).
        salt_set (str): The salt set to be used for hashing.

    Returns:
        str: The hashed result of the file.
    """
    if hashing_algorithm == "XOR":
        hash_result = XORHASH.xor_hash(file, salt_set)
    elif hashing_algorithm == "SHA":
        hash_result = SHA.sha_hash(file)
    else:
        print("Invalid hashing algorithm specified.")
        exit()
    
    return hash_result





def search_files(directory, hashing_algorithm, salt_set):
    """
    Searches for files in the given directory and hashes them.

    Args:
        directory (str): The directory to be searched for files.
        hashing_algorithm (str): The hashing algorithm to be used (XOR or SHA).
        salt_set (str): The salt set to be used for hashing.
    """
    with open('file_hashesV2.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Name', 'Full Path', 'Hash', 'Timestamp'])

        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                file_hash = hash_files(full_path, hashing_algorithm, salt_set)
                if file_hash is not None:
                    timestamp = time.ctime(os.path.getmtime(full_path))
                    csv_writer.writerow([file, full_path.replace("\\", "\\\\"), file_hash, timestamp])





def main(hashing_algorithm, salt_set):
    """
    Main function to initiate the file search and hashing process.

    Args:
        hashing_algorithm (str): The hashing algorithm to be used (XOR or SHA).
        salt_set (str): The salt set to be used for hashing.
    """
    

    directory = r"C:\Users\Arush Kathal\Desktop\CITS2006\Project\Ciphersystem\ExampleDir"
    search_files(directory, hashing_algorithm, salt_set)
    


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""Incorrect Usage. Usage: python3 RBAhashalgorithm.py [hashing_algorithm] [salt_set]
                        [hashing_algorithm] = XOR, 
                        [salt_set]          = keyset1 (for example)
                        """)
        exit()
        
        
    hashing_algorithm = sys.argv[1]
    salt_set = sys.argv[2]
    
    main(hashing_algorithm, salt_set)
