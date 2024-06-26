import os
import csv
import time
import struct

# Constants used in SHA-512
SHA512_CONSTANTS = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
]

# Initial hash values
INITIAL_HASH_VALUES = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
]

# Helper function to perform right rotation
def right_rotate(value, count, bits=64):
    rotated_value = (value >> count) | (value << (bits - count))
    rotated_value &= (1 << bits) - 1
    return rotated_value

# Function to compress a chunk of data
def sha512_compress(chunk, hash_values):
    message_schedule = list(struct.unpack('>16Q', chunk)) + [0] * 64
    for i in range(16, 80):
        s0 = right_rotate(message_schedule[i-15], 1) ^ right_rotate(message_schedule[i-15], 8) ^ (message_schedule[i-15] >> 7)
        s1 = right_rotate(message_schedule[i-2], 19) ^ right_rotate(message_schedule[i-2], 61) ^ (message_schedule[i-2] >> 6)
        message_schedule[i] = (message_schedule[i-16] + s0 + message_schedule[i-7] + s1) & ((1 << 64) - 1)

    a, b, c, d, e, f, g, h = hash_values

    for i in range(80):
        s1 = right_rotate(e, 14) ^ right_rotate(e, 18) ^ right_rotate(e, 41)
        choose = (e & f) ^ (~e & g)
        temp1 = (h + s1 + choose + SHA512_CONSTANTS[i] + message_schedule[i]) & ((1 << 64) - 1)
        s0 = right_rotate(a, 28) ^ right_rotate(a, 34) ^ right_rotate(a, 39)
        majority = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (s0 + majority) & ((1 << 64) - 1)

        h = g
        g = f
        f = e
        e = (d + temp1) & ((1 << 64) - 1)
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & ((1 << 64) - 1)

    updated_hash_values = [(x + y) & ((1 << 64) - 1) for x, y in zip(hash_values, [a, b, c, d, e, f, g, h])]
    return updated_hash_values

# Function to compute the SHA-512 hash of the input data
def sha512(data):
    """
    Compute the SHA-512 hash of the input data.

    This function processes the input data using the SHA-512 hashing algorithm. It first
    preprocesses the data by padding it according to the SHA-512 specification, then processes
    each 1024-bit chunk using the compression function, and finally produces a 512-bit hash value
    in hexadecimal format.

    Parameters:
    data (bytes): The input data to be hashed, provided as bytes.

    Returns:
    str: The hexadecimal representation of the SHA-512 hash value.
    """
    bit_length = len(data) * 8

    data += b'\x80'
    while (len(data) * 8) % 1024 != 896:
        data += b'\x00'

    data += struct.pack('>QQ', 0, bit_length)

    hash_values = INITIAL_HASH_VALUES[:]
    for i in range(0, len(data), 128):
        hash_values = sha512_compress(data[i:i+128], hash_values)

    final_hash = ''.join(f'{x:016x}' for x in hash_values)
    return final_hash[:50]

def hash_file(file_path):
    """
    Compute the SHA-512 hash of a file's contents.

    Parameters:
    file_path (str): The full path to the file to be hashed.

    Returns:
    str: The hexadecimal representation of the truncated or padded SHA-512 hash value (50 characters long).
    """
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return sha512(file_data)
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
def walk_directory_and_hash(directory):
    """
    Walk through a directory and hash each file, then write the results to a CSV file.

    Parameters:
    directory (str): The directory to walk through.

    Returns:
    None
    """
    with open('file_hashes.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Name', 'Full Path', 'Hash', 'Timestamp'])

        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                file_hash = hash_file(full_path)
                if file_hash is not None:
                    timestamp = time.ctime(os.path.getmtime(full_path))
                    csv_writer.writerow([file, full_path.replace("\\", "\\\\"), file_hash, timestamp])

# Example usage
if __name__ == "__main__":
    directory_to_walk = "C:\\Users\\olive\\OneDrive\\Desktop\\contractor work" # Replace directory path
    walk_directory_and_hash(directory_to_walk)
