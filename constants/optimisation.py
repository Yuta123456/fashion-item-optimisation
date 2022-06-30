WEIGHT = {
    # "com": 10/738,
    # "ver": 80,
    # "sim": 10/927,
    # "mul": 10/60,
    "com": 1,
    "sim": 2,
    "ver": 1,
    "mul": 9,
}

LAYER = 3
LAYER_NAME = ["top", "pants", "shoes"]
# 関数近似許容値 今は適当な数字
EPSILON = 1e-4
# 枚数の制約
TIME_STEP = 4

from enum import Enum
class Gender(Enum):
    MEN = "MEN"
    WOMEN = "WOMEN"
# ユーザの性別を指定
USER_GENDER = Gender("MEN")

# この二つの値は実験によって変える
SIMILARITY_THRESHOLD = 1.294459

SIGMA_B = -50

MEAN = {
    "com": -1000,
    "sim": 0.5305737461600649,
    # "sim": 0,
    "ver": 0.08375626872015988,
    "mul": 0.052145680162921544,
}
STD = {
    "com": 70.86691223171492,
    "sim": 0.21891407408552208,
    # "sim": 1,
    "ver": 0.004164577657076921,
    "mul": 0.10667910655956846,
}
