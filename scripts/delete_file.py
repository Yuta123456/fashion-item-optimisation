import sys
import os
import glob
delete_dir = sys.argv[1]

delete_file = glob.glob(delete_dir + "/*", recursive=True)

for p in delete_file:
    print(p)
    os.remove(p)
