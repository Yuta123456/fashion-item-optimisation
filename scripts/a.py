import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm 
file_path = "data/compatibility.txt"

x = pd.read_csv(file_path, sep="\n").loc[:500000]
df = pd.DataFrame(x, columns=['x'])
df["cumsum"] = df.x.cumsum() # 累積和を追加
df["cumsum_ratio"] = df.x.cumsum()/sum(df.x) # cumsumの値になるまでの確率
print(df)
print(df.describe())