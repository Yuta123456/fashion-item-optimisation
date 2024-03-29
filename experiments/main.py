# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import copy
import random
import sys
sys.path.append("D:\\fashion\\optimisation\\")


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

COUNT = 30
CLOSET_ITEM_NUM = 300
WEIGHT2 = {
    "com": 10/13,
    "sim": 5/4,
    "ver": 1.5,
    "mul": 1/3,
}
def optimization(weight):
    average_score = [0, 0, 0, 0]
    for _ in range(COUNT):
        all_items = [random.sample(original_all_items[i], CLOSET_ITEM_NUM) for i in range(LAYER)]
        select_items = init_closet(all_items, TIME_STEP)
        model.set_all_items(all_items)
        delta_obj = EPSILON + 1
        # ここから最適化
        obj = []
        pre_obj = 0
        while delta_obj >= EPSILON:
            for layer in range(LAYER):
                # 対象のレイヤを空に
                select_items[layer] = []
                for _t in range(TIME_STEP):
                    # sigmaはその際の増加分
                    sigma, additional_item = select_max_incremental_item(select_items, all_items,layer, model, weight)
                    # 増加分が最大となるアイテムを追加
                    select_items[layer].append(additional_item)
                obj.append(sigma)
            # 今回のループでの最適値はobj[LAYER-1][0]に格納されている。
            cur_obj = sum(calc_closet_score(select_items, model))
            delta_obj = cur_obj - pre_obj
            pre_obj = cur_obj
        score = calc_closet_score(select_items, model)
        for i, v in enumerate(score):
            average_score[i] += v
    average_score = list(map(lambda x: x/COUNT, average_score))
    return average_score
# 重みを変更させながら実行する必要がある。
w = copy.deepcopy(WEIGHT2)
w["com"] = 0
w["ver"] = 0
result = optimization(w)
print("drop_cv:com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*result))

w = copy.deepcopy(WEIGHT2)
w["mul"] = 0
result = optimization(w)
print("drop_m:com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*result))

w = copy.deepcopy(WEIGHT2)
w["sim"] = 0
result = optimization(w)
print("drop_s:com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*result))

w = copy.deepcopy(WEIGHT2)
w["sim"] = 0
w["mul"] = 0
result = optimization(w)
print("drop_sm:com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*result))

w = copy.deepcopy(WEIGHT2)
result = optimization(w)
print("full:com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*result))