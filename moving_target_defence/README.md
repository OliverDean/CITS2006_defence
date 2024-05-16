Uses a Python script (mtd_system.py) to monitor for events and trigger protection changes.
It logs when an MTD event is triggered but might not actually be changing the protection settings as expected.

It detects all 3 of these:
an alert has been raised by the Yara engine.

a file has been added/modified/deleted in the filesystem.
* you can test this with: echo "This is a new file." > ./ExampleDir/SubExampleDir/new_file.txt

a certain time interval has passed.
