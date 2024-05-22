import schedule
import time
import os
import sys
from datetime import datetime

def unpack_data(data_path):
    matchList = []
    pathDict, ruleDict = {}, {}
    #read through stored YARA data to compile matches found
    try:
        with open(data_path, 'r') as file:
            matches = file.readlines()
        for m in matches:
            rule, file = m.split(',')
            path = os.path.dirname(file)
            matchList.append((rule, path))
            pathDict.setdefault(path, 0)
            pathDict[path] += 1
            ruleDict.setdefault(rule, 0)
            ruleDict[rule] += 1
    except FileNotFoundError:
        print(f'Error: The file {data_path} does not exist.')
    except PermissionError:
        print(f'Error: Permission denied while accessing {data_path}.')
    except Exception as e:
        print(f'An error occurred: {e}')
        
    return matchList, pathDict, ruleDict
        

def generate_recommendations(output_dir, data_path):
    #use current date in filename and body to distinguish from previous recommendations
    date = datetime.now().strftime("%d-%m-%Y")
    file_content = f"RapidoBank Security System Log {date}\n\n"
    #get statistics from yara, mtd and add to file
    yara_matches, pathDict, ruleDict = unpack_data(data_path)
    yara_hits = len(yara_matches)

    file_content += (f"The YARA engine detected {yara_hits} potential vulnerabilities in the file system.\n")
    maxDir = max(pathDict, key=pathDict.get)
    file_content += (f"The directory \'{maxDir}\' contained {pathDict[maxDir]} vulnerabilities, the most out of any directory in the filesystem. Make sure no vulnerabilities exist that target this folder.\n")
    maxRule = max(ruleDict, key=ruleDict.get)
    file_content += (f"\'{maxRule}\' was the most common vulnerability detected, with {pathDict[maxDir]} found in the filesystem. Be sure to address this vulnerability directly so that malicious actors cannot exploit it.\n\n")
    
    if ruleDict.get('malware') + ruleDict.get('Complex_Code_Obfuscation') >= 3:
        file_content += (f"{ruleDict.get('malware') + ruleDict.get('Complex_Code_Obfuscation')} files were identified as potentially malware. Consider installing or updating antivirus software to reduce the likelihood of malware infecting your system.\n")
    if ruleDict.get('hidden_files') >= 3:
        file_content += (f"{ruleDict.get('hidden_files')} files were noted to be hidden but not encrypted. Make sure all files on the filesystem are encrypted, and avoid hiding files unless they have already been encrypted.\n")
    if ruleDict.get('network_executables') + ruleDict.get('urls') >= 3:
        file_content += (f"{ruleDict.get('network_executables') + ruleDict.get('urls')} files were identified as executables attempting to access network resources. Consider installing or updating firewalls and monitoring inbound and outbound network traffic to ensure no malicious actors are attempting to access your network.\n")
    if ruleDict.get('port_ssh') >= 3:
        file_content += (f"{ruleDict.get('port_ssh')} files were identified as attempting to scan ports and access SSH. Ensure that all ports not being actively used in the system are closed, and that any ports that are in use are monitored for attempted intrusions.\n")
    if ruleDict.get('Reconnaissance_Command_Execution') >= 3:
        file_content += (f"{ruleDict.get('Reconnaissance_Command_Execution')} files were identified as attempting to scan the network and identify its topology. Consider modifying the filesystem and isolating sensitive information to alter the topology and negate this attempt, and monitor the system carefully to detect attempted attacks.\n")
    
    #write the file
    filename = f"recommendations_{date}.txt"
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w") as file:
            file.write(file_content)
            print("The recommendation generation was successful.")
        #rename file once done so statistics are weekly
        os.rename(data_path, data_path[:-4] + str(datetime.now().strftime("%d-%m-%Y")) + ".txt")
    except PermissionError:
        print(f'Error: Permission denied while accessing {filepath}.')
    except Exception as e:
        print(f'An error occurred: {e}')

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short time to avoid high CPU usage


# Schedule recommendation creation every Sunday at midnight
#schedule.every().sunday.at("00:00").do(generate_recommendations)
# for demonstration increase recommendation creation speed
schedule.every(2).minutes.do(generate_recommendations)

#run with sudo python3 recommend.py match_data.txt (or a different path if you want the file in a different place; just make sure it matches with yara_engine.py)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 recommend.py <path_to_compiled_YARA_data>")
        sys.exit(1)
    # Ensure the file with YARA match data exists
    match_path = sys.argv[1]
    output_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(match_path):
        print(f'Error: The file {match_path} does not exist.')
        sys.exit(1)
    generate_recommendations(output_path, match_path)
    print("Scheduler started. Recommendations will be generated every Sunday at midnight.")
    run_scheduler()
