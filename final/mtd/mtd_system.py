import threading
import time
import logging
import monitor
import yara_monitor
import timer
import mtd_encryption
import mtd_decryption
import random
import json
import os
import signal

# Configure logging
logging.basicConfig(filename='mtd_system.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to save the previous settings
PREVIOUS_SETTINGS_FILE = 'previous_settings.json'

def load_previous_settings():
    if os.path.exists(PREVIOUS_SETTINGS_FILE):
        with open(PREVIOUS_SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return None

def save_previous_settings(cipher_system, keyset):
    with open(PREVIOUS_SETTINGS_FILE, 'w') as f:
        json.dump({'cipher_system': cipher_system, 'keyset': keyset}, f)

# Function to change protection settings
def change_protection_settings():
    logging.info("Entered change_protection_settings function")
    logging.info("Changing protection settings...")

    try:
        # Scan the directory to update files_to_skip lists
        logging.debug("Scanning directory for Yara matches...")
        yara_monitor.files_to_skip_encryption.clear()
        yara_monitor.files_to_skip_decryption.clear()
        yara_monitor.scan_directory(yara_monitor.rules, './ExampleDir/SubExampleDir')

        logging.debug(f"Files to skip encryption: {yara_monitor.files_to_skip_encryption}")
        logging.debug(f"Files to skip decryption: {yara_monitor.files_to_skip_decryption}")

        # Select a random cipher system and generate a new keyset
        logging.debug("Selecting a random cipher system...")
        new_cipher_system = random.choice(['XOR', 'RC4'])
        logging.info(f"New Cipher System: {new_cipher_system}")
        
        logging.debug("Generating a new keyset...")
        new_keyset = f'keyset{random.randint(1, 100)}'
        logging.info(f"New Keyset: {new_keyset}")

        logging.debug(f"Starting encryption with {new_cipher_system} and {new_keyset}")
        monitor.skip_mtd = True  # Set flag to skip MTD during encryption
        mtd_encryption.main(new_cipher_system, new_keyset, yara_monitor.files_to_skip_encryption)
        logging.debug("Encryption completed")
        monitor.skip_mtd = False  # Reset flag after encryption

        save_previous_settings(new_cipher_system, new_keyset)

        logging.info("Protection settings changed successfully.")
        logging.info("*****")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        logging.info("*****")

# Function to trigger MTD based on different events
def trigger_mtd(event_type):
    logging.info(f"Triggering MTD due to {event_type}")
    print(f"Triggering MTD due to {event_type}")
    change_protection_settings()

# Signal handler for clean shutdown
def handle_shutdown(signum, frame):
    logging.info("MTD System Stopped")
    print("MTD System Stopped")
    
    previous_settings = load_previous_settings()
    if previous_settings:
        previous_cipher_system = previous_settings['cipher_system']
        previous_keyset = previous_settings['keyset']
        logging.info(f"Decrypting with previous settings before shutdown: {previous_cipher_system}, {previous_keyset}")
        monitor.skip_mtd = True  # Set flag to skip MTD during decryption
        yara_monitor.files_to_skip_decryption.clear()
        yara_monitor.scan_directory(yara_monitor.rules, './ExampleDir/SubExampleDir')
        mtd_decryption.main(previous_cipher_system, previous_keyset, yara_monitor.files_to_skip_decryption)
        monitor.skip_mtd = False  # Reset flag after decryption
    else:
        logging.info("No previous settings found. Skipping decryption.")
    
    exit(0)

if __name__ == "__main__":
    logging.info("MTD System Started")
    print("MTD System Started")

    # Register signal handler for clean shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    monitor_thread = threading.Thread(target=monitor.start_monitoring, args=('./ExampleDir/',))
    monitor_thread.daemon = True
    monitor_thread.start()

    yara_monitor.rules = yara_monitor.load_yara_rules('./yara_rules')
    yara_thread = threading.Thread(target=yara_monitor.scan_directory, args=(yara_monitor.rules, './ExampleDir'))
    yara_thread.daemon = True
    yara_thread.start()

    interval =10  # Set a more reasonable time interval, e.g., 10 minutes
    timer_thread = threading.Thread(target=timer.periodic_trigger, args=(interval, trigger_mtd))
    timer_thread.daemon = True
    timer_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_shutdown(signal.SIGINT, None)
    logging.info("MTD System Stopped")
    print("MTD System Stopped")
