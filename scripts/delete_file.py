import sys
import os
import glob
delete_dir = sys.argv[1]

delete_file = glob.glob(delete_dir + "/**")

for p in delete_file:
    os.remove(p)
