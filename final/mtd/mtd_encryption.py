# mtd_encryption.py
import sys
import os
import XOR
import RC4

def encrypt_files(file, ciphersystem, cipherkeyset, files_to_skip):
    if file in files_to_skip:
        print(f'Skipping encryption for: {file}')
        return
    
    if ciphersystem == "XOR":
        XOR.xor_cipher(file, cipherkeyset, 'E')
    elif ciphersystem == "RC4":
        RC4.rc4_cipher(file, cipherkeyset, 'E')

    print("encrypted:", file)  # Only print this if the file is actually encrypted

def search_files(directory, ciphersystem, cipherkeyset, files_to_skip):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            encrypt_files(filepath, ciphersystem, cipherkeyset, files_to_skip)
        else:
            search_files(filepath, ciphersystem, cipherkeyset, files_to_skip)

def main(ciphersystem, cipherkeyset, files_to_skip):
    directory = r"./ExampleDir/SubExampleDir"
    search_files(directory, ciphersystem, cipherkeyset, files_to_skip)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Incorrect Usage. Usage: python3 main.py [ciphersystem] [cipherkeyset]
                                        [ciphersystem] = XOR, RC4
                                        [cipherkeyset] = keyset1 (for example)
                                        """)
        exit()
    ciphersystem = sys.argv[1]
    cipherkeyset = sys.argv[2]
    files_to_skip = set()
    main(ciphersystem, cipherkeyset, files_to_skip)
