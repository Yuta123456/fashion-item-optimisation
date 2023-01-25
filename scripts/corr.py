import pandas as pd
import numpy as np

def read_data(path):
    with open(path, mode="r") as f:
        res = [float(s.strip()) for s in f.readlines()]
    return res
com = read_data('data/rand_com.txt')
ver = read_data('data/rand_ver.txt')
sim = read_data('data/rand_sim.txt')
mul = read_data('data/rand_mul.txt')

N = len(com)
df = pd.DataFrame(index=['i'+str(i) for i in range(N)])
df['com'] = com
df['ver'] = ver
df['sim'] = sim
df['mul'] = mul
print(df.describe())
corr = df.corr()
print(corr)