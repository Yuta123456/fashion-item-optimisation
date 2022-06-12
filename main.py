# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import time
import uuid
from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_closet import init_closet
from util.save_closet import save_closet
from util_class.score_estimater import ScoreEstimater

from util.select_max_incremental_item import select_max_incremental_item
import tomotopy as tp
from util.init_all_item import init_all_item
import sys
import torch
from torchvision import models
import numpy as np
from PIL import Image
import torch.nn as nn


start = time.time()
all_items = init_all_item(LAYER, LAYER_NAME, 400)
select_items = init_closet(all_items, TIME_STEP)

delta_obj = EPSILON + 1
# [now_obj, pre_obj]
pre_obj = 0

# FashionItemの初期化

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
similarity_model = models.resnet18(pretrained=True)
num_ftrs = similarity_model.fc.in_features

similarity_model.fc = nn.Linear(num_ftrs,  738)

similarity_model.load_state_dict(torch.load('model.pth'))
model = ScoreEstimater(topic_model, all_items, similarity_model)

for i in range(LAYER):
    print(f"count of layer {LAYER_NAME[i]}: {len(all_items[i])}")
roop_cnt = 0
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
    print(calc_closet_score(select_items, model))
    delta_obj = cur_obj - pre_obj
    pre_obj = cur_obj
    roop_cnt += 1
    print(f"{roop_cnt}回目のループでの増加分{delta_obj}")

print(calc_closet_score(select_items, model))
try:
    closet_name = sys.argv[1]
except IndexError as e:
    closet_name = str(uuid.uuid1())[:6]
    print("クローゼットの名前の指定がありませんでした。")
    print(f"クローゼットの名前を{closet_name}で保存します")
    pass
save_closet(select_items, closet_name)
elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
