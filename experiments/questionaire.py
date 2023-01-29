# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import copy
import random
import sys

sys.path.append("D:\\fashion\\optimisation\\")


from util.show_fashion_images import show_fashion_images
from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_closet import init_closet
from util.save_closet import save_closet
from util_class.score_estimater import ScoreEstimater

from select_max_incremental_item_with_weight import select_max_incremental_item
import tomotopy as tp
from util.init_all_item import init_all_item
import torch
from torchvision import models
import torch.nn as nn


original_all_items = init_all_item(LAYER, LAYER_NAME, 400)
topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
similarity_model = models.resnet18(pretrained=True)
num_ftrs = similarity_model.fc.in_features

similarity_model.fc = nn.Linear(num_ftrs,  738)

similarity_model.load_state_dict(torch.load('model.pth'))
model = ScoreEstimater(topic_model, [[], [], []], similarity_model)

CLOSET_ITEM_NUM = 100
WEIGHT2 = {
    "com": 10/13,
    "sim": 5/4,
    "ver": 1.5,
    "mul": 1/3,
}
def optimization(weight, s_i, a_i, m):
    delta_obj = EPSILON + 1
    # ここから最適化
    obj = []
    pre_obj = 0
    while delta_obj >= EPSILON:
        print(delta_obj)
        for layer in range(LAYER):
            # 対象のレイヤを空に
            s_i[layer] = []
            for _t in range(TIME_STEP):
                # sigmaはその際の増加分
                sigma, additional_item = select_max_incremental_item(s_i, a_i,layer, m, weight)
                # 増加分が最大となるアイテムを追加
                s_i[layer].append(additional_item)
            obj.append(sigma)
        # 今回のループでの最適値はobj[LAYER-1][0]に格納されている。
        cur_obj = sum(calc_closet_score(s_i, m))
        delta_obj = cur_obj - pre_obj
        pre_obj = cur_obj
    return s_i

# file_names = ["mid"]
# score_names = ["mul"]


# for i in range(30):
#     for sn in score_names:
#         for fn in file_names:
#             w = copy.deepcopy(WEIGHT2)
#             w[sn] = 0
#             if fn == "high":
#                 w[sn] = 300
#             elif fn == "low":
#                 w[sn] = 0
#             fashion_items = optimization(w)
#             score = calc_closet_score(fashion_items, model)
#             print(score)
#             filename = fn + "_" + sn
#             if score[3] > 8 and score[3] < 10:
#                 with open("closet/" + filename, mode='a') as f:
#                     # 該当するレイヤーのアイテムだけ取得
#                     f.write(", ".join(map(str, score)) + "\n")
#                 save_closet(fashion_items, filename)
#                 exit()

drop_s_m = copy.deepcopy(WEIGHT2)
drop_s_m["sim"] = 0
drop_s_m["mul"] = 0
w = copy.deepcopy(WEIGHT2)
for i in range(5):
    all_items = [random.sample(original_all_items[i], CLOSET_ITEM_NUM) for i in range(LAYER)]
    select_items = init_closet(all_items, TIME_STEP)
    model.set_all_items(all_items)

    fashion_items = optimization(w, select_items, all_items, model)

    filename = "select_two_comp/test{}/".format(i+1) + "full_weight"
    
    save_closet(fashion_items, filename)

    fashion_items = optimization(drop_s_m, select_items, all_items, model)

    filename = "select_two_comp/test{}/".format(i+1) + "drop_s_m"
    
    save_closet(fashion_items, filename)