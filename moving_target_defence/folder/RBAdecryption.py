import sys
import os

import XOR
import RC4

def decrypt_files(file, ciphersystem, cipherkeyset):
    if ciphersystem == "XOR":
        XOR.xor_cipher(file, cipherkeyset, 'D')
    
    if ciphersystem == "RC4":
        RC4.rc4_cipher(file, cipherkeyset, 'D')            

def search_files(directory, ciphersystem, cipherkeyset):
    for filename in os.listdir(directory):  # Iterate over each file in the directory
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Check if the filepath is a file (not a directory)
            decrypt_files(filepath, ciphersystem, cipherkeyset)
            print("decrypted: ", filename)
        else:
            search_files(filepath, ciphersystem, cipherkeyset)  # If it's a directory, recursively search it

def main(ciphersystem, cipherkeyset):
    directory = r"./ExampleDir/SubExampleDir"
    search_files(directory, ciphersystem, cipherkeyset)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Incorrect Usage. Usage: python3 main.py [ciphersystem] [cipherkeyset]
                                        [ciphersystem] = XOR, RC4
                                        [cipherkeyset] = keyset1 (for example)
                                        """)
        exit()
        
    ciphersystem = sys.argv[1]
    cipherkeyset = sys.argv[2]
    
    main(ciphersystem, cipherkeyset) 
