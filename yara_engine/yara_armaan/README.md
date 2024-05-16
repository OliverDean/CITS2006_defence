yara_engine.py
Usage: python3 script_name.py <path_to_diretory_to_scan>

Loads and compiles Yara rules.
Scans specified directory recursively and prints matches.



updated yara_csv.py

1. The script reads each row in the CSV file and extracts the pattern strings.
2. It constructs a Yara rule using the extracted patterns, including metadata and condition sections.
3. The generated Yara rule is written to an output file.
The updated generates a file with the correct format to work with yara_engine.py 
