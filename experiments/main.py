# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import time
import uuid
import sys

from numpy import average
sys.path.append("D:\\fashion\\optimisation\\")


from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_closet import init_closet
from util.save_closet import save_closet
from util_class.score_estimater import ScoreEstimater

from util.select_max_incremental_item import select_max_incremental_item
import tomotopy as tp
from util.init_all_item import init_all_item
import torch
from torchvision import models
import torch.nn as nn

from util.save_closet import save_closet



all_items = init_all_item(LAYER, LAYER_NAME, 400)
topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
similarity_model = models.resnet18(pretrained=True)
num_ftrs = similarity_model.fc.in_features

similarity_model.fc = nn.Linear(num_ftrs,  738)

similarity_model.load_state_dict(torch.load('model.pth'))
model = ScoreEstimater(topic_model, all_items, similarity_model)

COUNT = 500
model = ScoreEstimater(topic_model, [[], [], []], similarity_model)

def optimization():
    average_score = [0, 0, 0, 0]
    for cnt in range(COUNT):
        select_items = init_closet(all_items, TIME_STEP)
        model.set_all_items(all_items)
        delta_obj = EPSILON + 1
        pre_obj = 0
        # ここから最適化
        while delta_obj >= EPSILON:
            for layer in range(LAYER):
                # 対象のレイヤを空に
                select_items[layer] = []
                for _t in range(TIME_STEP):
                    # sigmaはその際の増加分
                    _, additional_item = select_max_incremental_item(select_items, all_items,layer, model)
                    # 増加分が最大となるアイテムを追加
                    select_items[layer].append(additional_item)
            # 今回のループでの最適値はobj[LAYER-1][0]に格納されている。
            cur_obj = sum(calc_closet_score(select_items, model))
            # print(calc_closet_score(select_items, model))
            delta_obj = cur_obj - pre_obj
            pre_obj = cur_obj
            # print(f"{roop_cnt}回目のループでの増加分{delta_obj}")

        score = calc_closet_score(select_items, model)

        print("com:{:.2f} ver:{:.2f} sim:{:.2f} mul:{:.2f}".format(*score))
        cnt += 1
        if (cnt % 5 == 0):
            print(f"{cnt * 100 / COUNT}% 終了しました")
