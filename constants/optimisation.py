WEIGHT = {
    # "com": 10/738,
    # "ver": 80,
    # "sim": 10/927,
    # "mul": 10/60,
    "com": 1,
    "sim": 6,
    "ver": 1,
    "mul": 1,
}

LAYER = 3
LAYER_NAME = ["top", "pants", "shoes"]
# 関数近似許容値 今は適当な数字
EPSILON = 0.001
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
    "com": -4000,
    "sim": 0.865,
    "ver": 0.083,
    "mul": 0.164,
}
STD = {
    "com": 200,
    "sim": 0.42,
    "ver": 0.002,
    "mul": 0.117,
}
