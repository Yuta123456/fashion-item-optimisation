WEIGHT = {
    "com": 10/738,
    "ver": 80,
    "sim": 10/927,
    "mul": 10/60,
    # "com": 0,
    # "ver": 0,
    # "sim": 0,
    # "mul": 0,
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

threshold = 0.025112

SIGMA_B = 7