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

# Rest of the RC4.py code...





def ksa(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(S, data):
    i = j = 0
    keystream = []
    for _ in range(len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    return keystream

def encrypt(plaintext, key):
    keystream = prga(ksa(key), plaintext)
    encrypted_text = bytes(p ^ k for p, k in zip(plaintext, keystream))
    return encrypted_text

def decrypt(ciphertext, key):
    keystream = prga(ksa(key), ciphertext)
    decrypted_text = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    return decrypted_text

def RC4_ENCRYPTION(file, key):
    with open(file, 'rb') as f:
        original = f.read()
    encrypted = encrypt(original, key)
    with open(file, 'wb') as f:
        f.write(encrypted)

def RC4_DECRYPTION(file, key):
    with open(file, 'rb') as f:
        encrypted = f.read()
    decrypted = decrypt(encrypted, key)
    with open(file, 'wb') as f:
        f.write(decrypted)

def rc4_cipher(file, cipherkeyset, EncryptorDecrypt):
    key = load_key(cipherkeyset)
    if EncryptorDecrypt == "E":
        RC4_ENCRYPTION(file, key)
    elif EncryptorDecrypt == "D":
        RC4_DECRYPTION(file, key)
    else:
        print("IF/ELSE Error in RC4 cipher")
        exit()
