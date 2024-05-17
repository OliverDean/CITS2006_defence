# monitor.py
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'Modified: {event.src_path}')
        trigger_mtd('modified')

    def on_created(self, event):
        print(f'Created: {event.src_path}')
        trigger_mtd('created')

    def on_deleted(self, event):
        print(f'Deleted: {event.src_path}')
        trigger_mtd('deleted')

def start_monitoring(path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def trigger_mtd(event_type):
    print(f"Triggering MTD due to {event_type}")
    # Placeholder for MTD logic

if __name__ == "__main__":
    start_monitoring('./ExampleDir/SubExampleDir')

