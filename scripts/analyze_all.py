from copy import deepcopy
import pandas as pd 
import matplotlib.pyplot as plt
import math

def describe(filepath):
    df = pd.read_csv(filepath, sep="\n").loc[:500000]
    # df = df[df != 0].dropna()
    mean = df.mean().values[0]
    std = df.std().values[0]

    # 外れ値
    # df = df[(df <= mean + 3 * std)].dropna()
    df = df[(df >= mean - 3 * std)].dropna()

    # mean = df.mean().values[0]
    # std = df.std().values[0]
    # df = (df - mean) / std


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(df.values)
    plt.ylabel('frequency')
    plt.xlabel('index')
    plt.show()
    print(df.describe())
    return mean, std

mean, std = describe("data/com_w.txt")
print(f"==============compatibility===============\nmean: {mean} std: {std}\n====================================")
mean, std = describe("data/sim_w.txt")
print(f"===============similarity==============\nmean: {mean} std: {std}\n====================================")
mean, std = describe("data/ver_w.txt")
print(f"==============versatility==============\nmean: {mean} std: {std}\n====================================")
mean, std = describe("data/mul_w.txt")
print(f"==============multiply==============\nmean: {mean} std: {std}\n====================================")

# mean, std = describe("data/simirality.txt")
# print(f"==============similarity==============\nmean: {mean} std: {std}\n====================================")


# mean, std = describe("data/new_sim.txt")
# mean, std = describe("data/new_sim.txt")
# print(f"==============similarity==============\nmean: {mean} std: {std}\n====================================")
