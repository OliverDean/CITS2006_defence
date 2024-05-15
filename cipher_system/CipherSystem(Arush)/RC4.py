import random
import string

def generate_key():
    # Generate a random key of length 50 characters
    key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=50))
    return key

def save_key(cipher, key):
    with open('RBaEncryptionKeys.txt', 'a') as f:
        f.write(f"{cipher}:{key}\n")

def load_key(cipherkeyset):
    try:
        with open('RBaEncryptionKeys.txt', 'r+') as f:
            for line in f:
                cipher, key = line.strip().split(':')
                if cipher == cipherkeyset:
                    return key.encode()
        # If the cipherkeyset is not found, generate a new key and save it
        key = generate_key()
        save_key(cipherkeyset, key)
        return key.encode()
    except FileNotFoundError:
        # If the file doesn't exist, create it and return a new generated key
        key = generate_key()
        save_key(cipherkeyset, key)
        return key.encode()

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