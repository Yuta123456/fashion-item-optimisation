import pandas as pd

data = []
def read_data(path):
    with open(path, mode="r") as f:
        res = [float(s.strip()) for s in f.readlines()]
    return res
com = read_data('data/com.txt')
ver = read_data('data/ver.txt')
sim = read_data('data/sim.txt')
mul = read_data('data/mul.txt')
data = [[com[i], ver[i], sim[i], mul[i]] for i in range(len(com))]
# with open("data/ranking_data.txt", mode='r') as f:
#     data = [list(map(float, s.strip().split(" "))) for s in f.readlines()]
data = pd.DataFrame(data)
print(data.head())
print(data.describe())
print(data.corr())

print(data.corr(method = "spearman")) #スピアマン順位相関係数。
print(data.corr(method = "kendall")) #ケンドール順位相関係数。