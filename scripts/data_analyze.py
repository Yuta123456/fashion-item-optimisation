import pandas as pd 
import matplotlib.pyplot as plt
file_path = "data/multiply.txt"

df = pd.read_csv(file_path, sep="\n").loc[:500000]
# df = df.applymap(lambda x: x * 10**(-20))
df.hist(bins=100, color = "blue", grid =True, label = 'pandas')
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