import csv

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

# Usage example
create_yara_rule('string_exmpl.csv', 'generated_rule.yar', 'malware', 'Your Name')

