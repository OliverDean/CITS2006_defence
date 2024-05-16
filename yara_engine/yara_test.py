import yara
import os
import argparse

def load_rules(rules_directory):
    """Load all Yara rules from the specified directory and compile them."""
    rules = {}
    for root, dirs, files in os.walk(rules_directory):
        for file in files:
            if file.endswith(".yar"):
                path = os.path.join(root, file)
                try:
                    rule = yara.compile(path)
                    rules[path] = rule
                except yara.SyntaxError as e:
                    print(f"Failed to compile {path}: {e}")
    return rules

def scan_file(file_path, rules):
    """Scan a single file with all loaded Yara rules."""
    for rule_path, rule in rules.items():
        try:
            matches = rule.match(file_path)
            if matches:
                print(f"Match found in {file_path} by rules from {rule_path}")
        except yara.Error as e:
            print(f"Error scanning {file_path} with {rule_path}: {e}")

def scan_directory(target_directory, rules):
    """Scan all files in the target directory with loaded Yara rules."""
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                print(f"Scanning {path}...")
                scan_file(path, rules)

def main(args):
    """Load rules, scan directory, and report findings."""
    print("Loading Yara rules...")
    rules = load_rules(args.rules_directory)
    if rules:
        print(f"Loaded {len(rules)} rules.")
        print("Scanning target directory...")
        scan_directory(args.target_directory, rules)
        print("Scanning complete.")
    else:
        print("No rules were loaded, please check your rules directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Yara rules against a directory of files.')
    parser.add_argument('rules_directory', type=str, help='Directory where Yara rules (.yar files) are stored.')
    parser.add_argument('target_directory', type=str, help='Directory where files to be scanned are stored.')
    
    args = parser.parse_args()
    
    main(args)
