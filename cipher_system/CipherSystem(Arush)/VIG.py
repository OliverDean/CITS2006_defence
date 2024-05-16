import random
import string




def generate_key():
    # Generate a random key of length 50 characters
    key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=50))
    return key



def save_key(cipher, key):
    with open('RBaEncryptionKeys.txt', 'a') as f:
        f.write(f"{cipher}:{key}\n")
    
    pass




def load_key(cipherkeyset):
    try:
        with open('RBaEncryptionKeys.txt', 'r+') as f:
            for line in f:
                cipher, key = line.strip().split(':')
                if cipher == cipherkeyset:
                    return key
        # If the cipherkeyset is not found, generate a new key and save it
        key = generate_key()
        save_key(cipherkeyset, key)
        return key
    except FileNotFoundError:
        # If the file doesn't exist, create it and return a new generated key
        key = generate_key()
        save_key(cipherkeyset, key)
        
        return key
    
    pass



def vigenere_encrypt(key, plain_text):

    len_plain_text = len(plain_text)
    cipher_text = []

    key_len = len(key)
    range_size = 26 * 2  # considering both upper and lower case

    key_index = 0
    for i in range(len_plain_text):
        if plain_text[i].isalpha():
            if plain_text[i].islower():
                range_low = 'a'
            else:
                range_low = 'A'
            plain_offset = ord(plain_text[i]) - ord(range_low)
            key_offset = ord(key[key_index % key_len].lower()) - ord('a')
            cipher_text.append(chr((plain_offset + key_offset) % 26 + ord(range_low)))
            key_index += 1
        else:
            cipher_text.append(plain_text[i])

    cipher_text_str = ''.join(cipher_text)  # Convert list to string

    return cipher_text_str



def vigenere_decrypt(key, cipher_text):

    len_cipher_text = len(cipher_text)
    plain_text = []

    key_len = len(key)
    range_size = 26 * 2  # considering both upper and lower case

    key_index = 0
    for i in range(len_cipher_text):
        if cipher_text[i].isalpha():
            if cipher_text[i].islower():
                range_low = 'a'
            else:
                range_low = 'A'
            cipher_offset = ord(cipher_text[i]) - ord(range_low)
            key_offset = ord(key[key_index % key_len].lower()) - ord('a')
            plain_text.append(chr((cipher_offset - key_offset + 26) % 26 + ord(range_low)))
            key_index += 1
        else:
            plain_text.append(cipher_text[i])

    plain_text_str = ''.join(plain_text)  # Convert list to string

    return plain_text_str






def VIG_ENCRYPTION(file, key):
    
    
    with open(file, 'r') as f:
        original = f.read()

    encrypted = vigenere_encrypt(key, original)
    
    with open(file, 'w') as f:
        f.write(encrypted)   
    
    pass
    
    
def VIG_DECRYPTION(file, key):
    
    
    with open(file, 'r') as f:
        encrypted = f.read()
    
    decrypted = vigenere_decrypt(key, encrypted)

    with open(file, 'w') as f:
        f.write(decrypted)
    
    pass



def vig_cipher(file, cipherkeyset, EncryptorDecrypt):

    key = load_key(cipherkeyset)
    
    if EncryptorDecrypt == "E":
        VIG_DECRYPTION(file, key)
        
    elif EncryptorDecrypt == "D":
        VIG_ENCRYPTION(file, key)
        
    else:
        print("IF/ELSE Error in XOR.py: xor_cipher")
        exit()
        
        
    pass


    

# Example usage
# if __name__ == "__main__":
#     key_length = 50
#     key = generate_random_key(key_length)
#     plain_text = "The Prince of Egypt is a 1998 American animated musical drama film produced by DreamWorks Animation and distributed by DreamWorks Pictures. The second feature film from DreamWorks and the first to be traditionally animated, it is an adaptation of the Book of Exodus and follows the life of Moses from being a prince of Egypt to a prophet chosen by God to carry out his ultimate destiny of leading the Hebrews out of Egypt."
# 
#     # Encrypt
#     status, cipher_text = vigenere_encrypt(key, plain_text)
#     if status == 0:
#         print(f"Cipher text: {cipher_text}")
#     else:
#         print("Encryption failed.")
# 
#     # Decrypt
#     status, decrypted_text = vigenere_decrypt(key, cipher_text)
#     if status == 0:
#         print(f"Decrypted text: {decrypted_text}")
#     else:
#         print("Decryption failed.")