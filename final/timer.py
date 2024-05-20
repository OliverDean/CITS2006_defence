# timer.py
import time
import threading
import logging

def periodic_trigger(interval, trigger_mtd):
    while True:
        trigger_mtd('time interval')
        time.sleep(interval)

if __name__ == "__main__":
    interval = 10  # 10 seconds for testing
    timer_thread = threading.Thread(target=periodic_trigger, args=(interval, lambda event_type: print(f"Triggering MTD due to {event_type}")))
    timer_thread.daemon = True
    timer_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
