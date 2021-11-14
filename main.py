# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import glob
from util.show_fashion_images import show_fashion_images
from util_class.score_estimater import ScoreEstimater

from util.select_max_incremental_item import select_max_incremental_item
from PIL import Image
import tomotopy as tp
from util.init_all_item import init_all_item 
LAYER = 3
LAYER_NAME = ["top", "pants", "shoes"]
# 関数近似許容値 今は適当な数字
EPSILON = 0.01
# 枚数の制約
TIME_STEP = 4
select_items = [[] for i in range(LAYER)]
all_items = [[] for i in range(LAYER)]
models = None
delta_obj = EPSILON + 1
# [now_obj, pre_obj] 
obj = [[0, 0] for i in range(LAYER)]

# FashionItemの初期化
all_items = init_all_item(LAYER, LAYER_NAME)

# TODO: model init
topic_model = tp.LDAModel.load('lda_model.bin')

model = ScoreEstimater(topic_model, all_items)
for i in range(LAYER):
    print(f"count of layer {LAYER_NAME[i]}: {len(all_items[i])}")
while delta_obj >= EPSILON:
    for layer in range(LAYER):
        select_items[layer] = []
        obj[layer][0] = 0
        for time in range(TIME_STEP):
            # sigmaはその際の増加分
            sigma, additional_item = select_max_incremental_item(select_items, all_items,layer, model)
            # 増加分が最大となるアイテムを追加
            select_items[layer].append(additional_item)
            obj[layer][0] += sigma
    # 今回のループでの最適値はobj[LAYER-1][0]に格納されている。
    delta_obj = obj[LAYER-1][0] - obj[LAYER-1][1]
    obj[LAYER-1][1] = obj[LAYER-1][0]
show_fashion_images(select_items)