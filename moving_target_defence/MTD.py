import os
import time
import subprocess
import random
import sys

def encrypt_files(directory, ciphersystem, cipherkeyset):
    # Call RBAencryption.py to encrypt files
    subprocess.run(["python", "RBAencryption.py", ciphersystem, cipherkeyset])

def decrypt_files(directory, ciphersystem, cipherkeyset):
    # Call RBAdecryption.py to decrypt files
    subprocess.run(["python", "RBAdecryption.py", directory, ciphersystem, cipherkeyset])

def change_encryption_method(current_method):
    # Implement code to change encryption method
    # For demonstration, let's rotate between XOR, DES, and RC4
    encryption_methods = ["XOR", "DES", "RC4"]
    new_method = random.choice(encryption_methods)
    while new_method == current_method:  # Ensure the new method is different from the current one
        new_method = random.choice(encryption_methods)
    return new_method

def main(directory, ciphersystem, cipherkeyset):
    current_method = ciphersystem
    while True:
        try:
            decrypt_files(directory, ciphersystem, cipherkeyset)  # Decrypt files
            current_method = change_encryption_method(current_method)  # Change encryption method
            encrypt_files(directory, current_method, cipherkeyset)  # Encrypt files with new method
            time.sleep(3600)  # Sleep for an hour (3600 seconds)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Incorrect Usage. Usage: python3 MTD.py [directory] [ciphersystem] [cipherkeyset]")
        exit()
        
    directory = sys.argv[1]
    ciphersystem = sys.argv[2]
    cipherkeyset = sys.argv[3]
    
    main(directory, ciphersystem, cipherkeyset) 
