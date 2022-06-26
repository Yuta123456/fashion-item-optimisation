# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import sys
import time
from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_closet import init_closet
from util.record_data import record_data
from util_class.score_estimater import ScoreEstimater

from util.select_max_incremental_item import select_max_incremental_item
import tomotopy as tp
from util.init_all_item import init_all_item
import torch
from torchvision import models
import torch.nn as nn
import random

# start = time.time()
original_all_items = init_all_item(LAYER, LAYER_NAME, 200)

# FashionItemの初期化

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
similarity_model = models.resnet18(pretrained=True)
num_ftrs = similarity_model.fc.in_features

similarity_model.fc = nn.Linear(num_ftrs, 738)

similarity_model.load_state_dict(torch.load('model.pth'))

if "--clear" in sys.argv:
    with open("data/com.txt", mode="w") as f:
        f.write("")
    with open("data/sim.txt", mode="w") as f:
        f.write("")
    with open("data/ver.txt", mode="w") as f:
        f.write("")
    with open("data/mul.txt", mode="w") as f:
        f.write("")
    print("data clear run")
COUNT = 10000
CLOSET_ITEM_NUM = 40
model = ScoreEstimater(topic_model, [[], [], []], similarity_model)
for cnt in range(COUNT):
    all_items = [random.sample(original_all_items[i], CLOSET_ITEM_NUM) for i in range(LAYER)]
    # closet.append(random.sample(all_items[i], 4))
    select_items = init_closet(all_items, TIME_STEP)
    model.set_all_items(all_items)
    delta_obj = EPSILON + 1
    pre_obj = 0 
    # ここから最適化
    while delta_obj >= EPSILON:
        for layer in range(LAYER):
            select_items[layer] = []
            for t in range(TIME_STEP):
                # sigmaはその際の増加分
                sigma, additional_item = select_max_incremental_item(select_items, all_items,layer, model)
                # 増加分が最大となるアイテムを追加
                select_items[layer].append(additional_item)
        # 今回のループでの最適値はobj[LAYER-1][0]に格納されている。
        cur_obj = sum(calc_closet_score(select_items, model))
        # print(calc_closet_score(select_items, model))
        delta_obj = cur_obj - pre_obj
        pre_obj = cur_obj
        # print(f"{roop_cnt}回目のループでの増加分{delta_obj}")

    score = calc_closet_score(select_items, model)
    record_data("data/com.txt", score[0])
    record_data("data/ver.txt", score[1])
    record_data("data/sim.txt", score[2])
    record_data("data/mul.txt", score[3])
    print("com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*score))
    cnt += 1
    if (cnt % 5 == 0):
        print(f"{cnt * 100 / COUNT}% 終了しました")
