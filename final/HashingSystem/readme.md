explains how to use in usage error statement

you're suppose to run  RBAhashalgorithms.py which outputs a CSV, then modify the files if wanted, then run RBATestHashedCsv.py (does the exact same thing but creates another CSV), and then compare_hashes.py to just compare both CVS files



When i tested it, a lot of the times the old file and new file would produce the same hash. Not sure if that was just for me, if someone else can have a look at it that would be great 🙏


Some notes:
- the XOR hash takes quite a while for me (like 15 - 20 seconds). Someone could have a look at this if they have time.
- many times, changing the files contents still produces the same hash. This might be an easy fix, I didn't have time to
  look into it yet. 
