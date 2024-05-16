# RapidoBank Encryption System


Our system supports the following ciphers:
- **XOR**
- **DES**
- **Vigenère (VIG)**
- **RC4**

You can use these ciphers to encrypt and decrypt files in a specified directory. The keys are stored in a file, and the system can generate new keys if needed.

# File Structure

.
├── DES.py
├── RC4.py
├── VIG.py
├── XOR.py
├── RBAencryption.py
├── RBAdecryption.py
├── RBaEncryptionKeys.txt
└── ExampleDir
└── SubExampleDir
└── testfile.txt

# Encrypt
~python3 RBAencryption.py [directory] [ciphersystem] [cipherkeyset]

e.g. python3 RBAencryption.py ./ExampleDir/SubExampleDir/ XOR keyset1


# Decrypt

python3 RBAdecryption.py [directory] [ciphersystem] [cipherkeyset]

e.g. python3 RBAdecryption.py ./ExampleDir/SubExampleDir XOR keyset1


Added Directory Input: Now you can specify a directory, and the system will recursively encrypt/decrypt all files within it.
