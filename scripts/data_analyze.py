import pandas as pd 
import matplotlib.pyplot as plt
import math
file_path = "data/sim.txt"

df = pd.read_csv(file_path, sep="\n").loc[:500000]
# df = df.applymap(lambda x: x * 10**(25))
# df.hist(bins=100, color = "blue", grid =True, label = 'pandas')

mean = df.mean().values[0]
std = df.std().values[0]

# 外れ値
df = df[(df <= mean + 3 * std)].dropna()
df = df[(df >= mean - 3 * std)].dropna()

mean = df.mean().values[0]
std = df.std().values[0]
# df = (df - mean) / std


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.hist(df.values)
plt.ylabel('frequency')
plt.xlabel('index')
plt.show()
print(df.describe())