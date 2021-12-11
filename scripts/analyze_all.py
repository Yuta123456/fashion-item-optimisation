from copy import deepcopy
import pandas as pd 
import matplotlib.pyplot as plt
import math

def describe(filepath):
    df = pd.read_csv(filepath, sep="\n").loc[:500000]
    df = df[df != 0].dropna()
    dmin = df.min().values[0]
    dmax = df.max().values[0]
    # df = df.applymap(lambda x:(x - (dmin))/(dmax - dmin))
    print(dmin, dmax)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(df.values)
    plt.ylabel('frequency')
    plt.xlabel('index')
    plt.show()
    print(df.describe())

describe("data/compatibility.txt")
describe("data/simirality.txt")
describe("data/versatility.txt")
describe("data/multiply.txt")
describe("data/log_compatibility.txt")