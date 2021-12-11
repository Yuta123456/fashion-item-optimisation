# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3

from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.save_closet import save_closet
from util_class.score_estimater import ScoreEstimater

from util.select_max_incremental_item import select_max_incremental_item
import tomotopy as tp
from util.init_all_item import init_all_item

select_items = [[] for i in range(LAYER)]
all_items = [[] for i in range(LAYER)]

delta_obj = EPSILON + 1
# [now_obj, pre_obj]
pre_obj = 0

# FashionItemの初期化
all_items = init_all_item(LAYER, LAYER_NAME, 100)

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')

model = ScoreEstimater(topic_model, all_items)
for i in range(LAYER):
    print(f"count of layer {LAYER_NAME[i]}: {len(all_items[i])}")
roop_cnt = 0
while delta_obj >= EPSILON:
    for layer in range(LAYER):
        select_items[layer] = []
        for time in range(TIME_STEP):
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
save_closet(select_items, "yuta_tanaka")

