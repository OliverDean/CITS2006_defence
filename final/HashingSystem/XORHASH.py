import os
import random
import string

SALT_FILE = "RBaHashingSalt.txt"
SECRET_KEY_FILE = "RBaSecretKey.txt"



def generate_salt():
    # Generate a random string of ASCII characters
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    return salt



def load_salt(salt_set):
    # Load salt from file or generate a new one if not found
    try:
        with open(SALT_FILE, 'r+') as f:
            for line in f:
                value, salt = line.strip().split(':')
                if value == salt_set:
                    return salt
        # If the salt set is not found, generate a new salt and save it
        salt = generate_salt()
        save_salt(salt_set, salt)
        return salt
    except FileNotFoundError:
        # If the file doesn't exist, create it and return a new generated salt
        salt = generate_salt()
        save_salt(salt_set, salt)
        return salt



def save_salt(salt_set, salt):
    # Save salt to file
    with open(SALT_FILE, 'a') as f:
        f.write(f"{salt_set}:{salt}\n")
        



def generate_secret_key():
    # Generate a random string of ASCII characters for the secret key
    secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    return secret_key




def load_secret_key():
    # Load secret key from file or generate a new one if not found
    try:
        with open(SECRET_KEY_FILE, 'r') as f:
            secret_key = f.read().strip()
            return secret_key
    except FileNotFoundError:
        # If the file doesn't exist, generate a new secret key and save it
        secret_key = generate_secret_key()
        save_secret_key(secret_key)
        return secret_key




def save_secret_key(secret_key):
    # Save secret key to file
    with open(SECRET_KEY_FILE, 'w') as f:
        f.write(secret_key)
        
        
        

def hash_function(binary_content, secret_key, salt):
    # Hash function to calculate hash value of binary content
    hash_value = 0
    
    # Convert secret key to integer value
    secret_key_int = int.from_bytes(secret_key.encode(), byteorder='big')
    
    # Convert salt to integer value
    salt_int = int.from_bytes(salt.encode(), byteorder='big')
    
    # Iterate over each byte in the binary content
    for byte in binary_content:
        # Update hash value using bitwise XOR operation with byte value, secret key, and salt
        hash_value ^= (byte + secret_key_int + salt_int)
        
        # Add some additional mixing for better dispersion of bits
        hash_value = (hash_value << 5) + (hash_value >> 2)
    
    # Convert hash value to hexadecimal representation
    hex_hash = hex(hash_value)
    
    # Truncate the hash to 50 characters
    truncated_hash = hex_hash[2:52]  # Exclude '0x' prefix and ensure 50 characters
    
    return truncated_hash




def xor_hash(file, salt_set):
    # Calculate hash using XOR algorithm
    salt = load_salt(salt_set)
    secret_key = load_secret_key()  # Load the secret key
    with open(file, 'rb') as f:  # Open file in binary mode for reading
        binary_content = f.read()  # Read binary content
    hash_result = hash_function(binary_content, secret_key, salt)
    return hash_result