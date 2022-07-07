import sys
sys.path.append("D:\\fashion\\optimisation\\")
from constants.optimisation import MEAN, STD
import pandas as pd
data = []
with open("./data/ver.txt") as f:
    for line in f.readlines():
        value = float(line)
        data.append(value)

raw_data = list(map(lambda x: x *  STD["ver"] + MEAN["ver"], data))
raw_data = pd.DataFrame(data=raw_data)

print(raw_data.describe())
