import csv

def compare_hashes(file1, file2):
    """
    Compares hashes between two CSV files and prints any files with non-matching hashes.

    Args:
        file1 (str): Path to the first CSV file.
        file2 (str): Path to the second CSV file.
    """
    # Dictionary to store hashes from file1
    hash_dict1 = {}
    # Dictionary to store hashes from file2
    hash_dict2 = {}

    # Read and store hashes from file1
    with open(file1, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            file_name = row[0]
            file_hash = row[2]
            hash_dict1[file_name] = file_hash

    # Read and store hashes from file2
    with open(file2, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            file_name = row[0]
            file_hash = row[2]
            hash_dict2[file_name] = file_hash

    # Compare hashes and print non-matching files
    for file_name in hash_dict1:
        if file_name in hash_dict2:
            if hash_dict1[file_name] != hash_dict2[file_name]:
                print(f"{file_name} non-matching hashes detected:\nfile_hashes: {hash_dict1[file_name]}\nfile_hashesV2.csv: {hash_dict2[file_name]}\n")

# Usage example
compare_hashes("file_hashes.csv", "file_hashesV2.csv")