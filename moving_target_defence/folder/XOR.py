import random
import string
import logging

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=50))

def save_key(cipher, key):
    with open('RBaEncryptionKeys.txt', 'a', encoding='utf-8') as f:
        escaped_key = key.replace('\\', '\\\\').replace(':', '\\:')
        f.write(f"{cipher}:{escaped_key}\n")

def load_key(cipherkeyset):
    try:
        with open('RBaEncryptionKeys.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    cipher, key = parts
                    if cipher == cipherkeyset:
                        return key.replace('\\:', ':').replace('\\\\', '\\').encode()
                else:
                    logging.error(f"Incorrectly formatted line in key file: {line}")
        key = generate_key()
        save_key(cipherkeyset, key)
        return key.encode()
    except FileNotFoundError:
        key = generate_key()
        save_key(cipherkeyset, key)
        return key.encode()
    except Exception as e:
        logging.error(f"Error loading key: {e}")
        raise

# Rest of the XOR.py code...




def encrypt(plaintext, key):
    encrypted_text = b''
    for i in range(len(plaintext)):
        # XOR each byte of plaintext with corresponding byte of key
        encrypted_byte = plaintext[i] ^ key[i % len(key)]
        encrypted_text += bytes([encrypted_byte])
    return encrypted_text



def decrypt(ciphertext, key):
    decrypted_text = b''
    for i in range(len(ciphertext)):
        # XOR each byte of ciphertext with corresponding byte of key
        decrypted_byte = ciphertext[i] ^ key[i % len(key)]
        decrypted_text += bytes([decrypted_byte])
    return decrypted_text





def XOR_ENCRYPTION(file, key):
    
    with open(file, 'rb') as f:
        original = f.read()

    encrypted = encrypt(original, key)
    
    with open(file, 'wb') as f:
        f.write(encrypted)   
    
    
    
    
    
def XOR_DECRYPTION(file, key):
    
    with open(file, 'rb') as f:
        encrypted = f.read()

    decrypted = decrypt(encrypted, key)

    with open(file, 'wb') as f:
        f.write(decrypted)
    
    
    
    

def xor_cipher(file, cipherkeyset, EncryptorDecrypt):
    
    key = load_key(cipherkeyset)
    
    if EncryptorDecrypt == "E":
        XOR_ENCRYPTION(file, key)
        
    elif EncryptorDecrypt == "D":
        XOR_DECRYPTION(file, key)
        
    else:
        print("IF/ELSE Error in XOR.py: xor_cipher")
        exit()
        
        
    pass
        
        
        
        
        
        
        
        
        
