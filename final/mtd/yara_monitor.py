# yara_monitor.py
import yara
import os
import logging

files_to_skip_encryption = []
files_to_skip_decryption = []

def load_yara_rules(rules_directory):
    rules = {}
    for filename in os.listdir(rules_directory):
        if filename.endswith('.yar'):
            rule_path = os.path.join(rules_directory, filename)
            try:
                logging.info(f'Compiling Yara rule: {rule_path}')
                rule = yara.compile(filepath=rule_path)
                rules[filename] = rule
            except yara.SyntaxError as e:
                logging.error(f'Syntax error in {rule_path}: {e}')
            except yara.Error as e:
                logging.error(f'Error compiling {rule_path}: {e}')
    return rules

def scan_file(rules, file_path):
    if not os.path.isfile(file_path):
        logging.error(f'Error: The file {file_path} does not exist.')
        return

    logging.info(f'Scanning file: {file_path}')
    for rule_name, rule in rules.items():
        matches = rule.match(file_path)
        if matches:
            logging.info(f'Match found in {file_path} for rule {rule_name}:')
            files_to_skip_encryption.append(file_path)
            files_to_skip_decryption.append(file_path)
            for match in matches:
                logging.info(f'  Rule: {match.rule}')
                for string in match.strings:
                    logging.info(f'    String matched: {string}')
                    # Extract the matched content
                    with open(file_path, 'rb') as f:
                        f.seek(string[0])
                        matched_content = f.read(len(string[2]))
                        logging.info(f'    Matched content: {matched_content}')

def scan_directory(rules, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            scan_file(rules, file_path)

def trigger_mtd(event_type):
    logging.info(f"Triggering MTD due to {event_type}")
    change_protection_settings()

def change_protection_settings():
    logging.info("Changing protection settings...")
    # Implement the logic to change encryption keys, hashing algorithms, or cipher systems

if __name__ == "__main__":
    rules_directory = './yara_rules'
    rules = load_yara_rules(rules_directory)
    
    # Path to the file to scan
    directory_to_scan = './ExampleDir'
    
    # Scan the directory
    scan_directory(rules, directory_to_scan)
