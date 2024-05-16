import sys
import os

import XOR
import DES
import VIG
import RC4

def decrypt_files(file, ciphersystem, cipherkeyset):
    if ciphersystem == "XOR":
        XOR.xor_cipher(file, cipherkeyset, 'D')
    elif ciphersystem == "DES":
        DES.des_cipher(file, cipherkeyset, 'D')
    elif ciphersystem == "VIG":
        VIG.vig_cipher(file, cipherkeyset, 'D')
    elif ciphersystem == "RC4":
        RC4.rc4_cipher(file, cipherkeyset, 'D')

def search_files(directory, ciphersystem, cipherkeyset):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            decrypt_files(filepath, ciphersystem, cipherkeyset)
            print("decrypted:", filename)
        else:
            search_files(filepath, ciphersystem, cipherkeyset)

def main(directory, ciphersystem, cipherkeyset):
    search_files(directory, ciphersystem, cipherkeyset)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("""Incorrect Usage. Usage: python3 RBAdecryption.py [directory] [ciphersystem] [cipherkeyset]
                              [directory] = path to directory
                              [ciphersystem] = XOR, DES, VIG, RC4
                              [cipherkeyset] = keyset1 (for example)
               """)
        exit()

    directory = sys.argv[1]
    ciphersystem = sys.argv[2]
    cipherkeyset = sys.argv[3]

    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        exit()

    main(directory, ciphersystem, cipherkeyset)

