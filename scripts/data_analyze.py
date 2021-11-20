import pandas as pd 
import matplotlib.pyplot as plt
file_path = "data/versatility.txt"

df = pd.read_csv(file_path, sep="\n").loc[:500000]
# df = df.applymap(lambda x: x * 10**(-20))
df.hist(bins=1000, color = "blue", grid =True, label = 'pandas')
mean = 0.762482
# std              0.061218
# min              0.666116
# 25%              0.712959
# 50%              0.746619
# 75%              0.791317
# max              0.921980
data = df[df > (mean + 0.061218 * 2)].dropna()
print(data)
plt.ylabel('frequency')
plt.xlabel('index')
plt.legend()
# plt.ylim(0, 2000)
# plt.xlim(0, 2.0*(10**(-13)))
plt.title('pandas_histgram_norm')
plt.savefig("pandas_hist.png")
plt.show()

plt.close()
print(df.describe())