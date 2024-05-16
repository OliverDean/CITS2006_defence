# yara_monitor.py
import yara
import os

def load_yara_rules(rules_directory):
    rules = {}
    for filename in os.listdir(rules_directory):
        if filename.endswith('.yar'):
            rule_path = os.path.join(rules_directory, filename)
            try:
                print(f'Compiling Yara rule: {rule_path}')
                rule = yara.compile(filepath=rule_path)
                rules[filename] = rule
            except yara.SyntaxError as e:
                print(f'Syntax error in {rule_path}: {e}')
            except yara.Error as e:
                print(f'Error compiling {rule_path}: {e}')
    return rules

def scan_file(rules, file_path):
    if not os.path.isfile(file_path):
        print(f'Error: The file {file_path} does not exist.')
        return

    print(f'Scanning file: {file_path}')
    for rule_name, rule in rules.items():
        matches = rule.match(file_path)
        if matches:
            print(f'Match found in {file_path} for rule {rule_name}:')
            trigger_mtd('Yara alert')
            for match in matches:
                print(f'  Rule: {match.rule}')
                for string in match.strings:
                    print(f'    String matched: {string}')

def trigger_mtd(event_type):
    print(f"Triggering MTD due to {event_type}")
    change_protection_settings()

def change_protection_settings():
    print("Changing protection settings...")
    # Implement the logic to change encryption keys, hashing algorithms, or cipher systems

if __name__ == "__main__":
    rules_directory = './yara_rules'
    rules = load_yara_rules(rules_directory)
    
    # Path to the file to scan
    file_to_scan = './ExampleDir/SubExampleDir/test_malware.txt'
    
    # Scan the file
    scan_file(rules, file_to_scan)

