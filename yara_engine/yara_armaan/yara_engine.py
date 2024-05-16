import yara
import os
import csv
import sys

def create_yara_rule(csv_filepath, output_filepath, rule_name, author):
    try:
        with open(csv_filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            strings_section = []
            meta_section = f'\tdescription = "Rule to detect malware based on specific strings"\n\tauthor = "{author}"\n'

            for i, row in enumerate(reader):
                if row:
                    safe_string = csv_escape(row[0])
                    strings_section.append(f'\t$string{i} = "{safe_string}" nocase')

            yara_rule = (
                f'rule {rule_name}\n{{\n'
                f'\tmeta:\n{meta_section}'
                f'\tstrings:\n' + '\n'.join(strings_section) + '\n\n'
                f'\tcondition:\n\t\tany of them\n'
                f'}}'
            )

            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(yara_rule)

            print(f'Yara rule written to {output_filepath}')

    except FileNotFoundError:
        print(f'Error: The file {csv_filepath} does not exist.')
    except PermissionError:
        print(f'Error: Permission denied while accessing {csv_filepath}.')
    except Exception as e:
        print(f'An error occurred: {e}')

def csv_escape(s):
    return s.replace('"', '""').replace('\n', ' ').replace('\r', ' ')

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
    print(f'Scanning file: {file_path}')
    for rule_name, rule in rules.items():
        matches = rule.match(file_path)
        if matches:
            print(f'Match found in {file_path} for rule {rule_name}:')
            for match in matches:
                print(f'  Rule: {match.rule}')
                for string in match.strings:
                    print(f'    String matched: {string}')

def scan_directory(rules, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            scan_file(rules, file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <path_to_directory_to_scan>")
        sys.exit(1)

    directory_to_scan = sys.argv[1]

    # Ensure the directory to scan exists
    if not os.path.exists(directory_to_scan):
        print(f'Error: The directory {directory_to_scan} does not exist.')
        sys.exit(1)

    # Current directory where all files are stored
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create Yara rule from CSV
    create_yara_rule(os.path.join(current_directory, 'string_exmpl.csv'), os.path.join(current_directory, 'generated_rule.yar'), 'malware', 'Your Name')

    # Directory where Yara rules are stored
    rules_directory = current_directory

    # Load Yara rules
    rules = load_yara_rules(rules_directory)

    # Scan the directory recursively
    scan_directory(rules, directory_to_scan)

