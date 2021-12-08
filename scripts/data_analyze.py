import pandas as pd 
import matplotlib.pyplot as plt
import math
file_path = "data/compatibility.txt"

df = pd.read_csv(file_path, sep="\n").loc[:500000]
# df = df.applymap(lambda x: x * 10**(25))
# df.hist(bins=100, color = "blue", grid =True, label = 'pandas')
mean = df.mean().values[0]
std = df.std().values[0]

print(mean, std)
df = df[df != 0].dropna()
df = df[(df <= mean + 2 * std)].dropna()
df = df[(df >= mean - 2 * std)].dropna()
dmin = df.min().values[0]
dmax = df.max().values[0]
df = df.applymap(lambda x:(x - (dmin))/(dmax - dmin))
# print(df)
# count  3.618000e+03
# mean   4.670612e-12
# std    4.427591e-11
# min    9.170126e-27
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.hist(df.values)
plt.ylabel('frequency')
plt.xlabel('index')
plt.show()
print(df.describe())