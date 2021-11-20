# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import glob
import itertools
import pathlib
from PIL import Image
import tomotopy as tp
import sys
import datetime
sys.path.append("D:\\fashion\\optimisation\\")
from util_class.score_estimater import ScoreEstimater
from util.init_all_item import init_all_item 
LAYER = 3
LAYER_NAME = ["top", "pants", "shoes"]
# 枚数の制約
TIME_STEP = 4
all_items = [[] for i in range(LAYER)]
models = None

# FashionItemの初期化
all_items = init_all_item(LAYER, LAYER_NAME, 300)

# TODO: model init
topic_model = tp.LDAModel.load('./lda_model.bin')

model = ScoreEstimater(topic_model, all_items)
coodinate_count = 0
all_coodinate_count = 1
for i in range(LAYER):
    print(f"count of layer {LAYER_NAME[i]}: {len(all_items[i])}")
    all_coodinate_count *= len(all_items[i])
for top in all_items[0]:
    for pants in all_items[1]:
        for shoes in all_items[2]:
            coodinate = [top, pants, shoes]
            compatibility_score = model.estimate_coodinate_compatibility(coodinate)
            versatility_score = model.estimate_versatility_score([coodinate])
            with open("data/compatibility.txt", mode='a') as f:
                f.write(str(compatibility_score) + "\n")
            with open("data/versatility.txt", mode='a') as f:
                f.write(str(versatility_score) + "\n")
            coodinate_count += 1
            if coodinate_count % 10000 == 0:
                print(f"finish coodinate : {coodinate_count * 100 / all_coodinate_count} % {datetime.datetime.now()}")

for layer_items in all_items:
    for pair in itertools.combinations(layer_items, 2):
        similarity_score = model.calc_image_similarity(pair[0], pair[1])
        with open("data/similarity.txt", mode='a') as f:
            f.write(str(similarity_score) + "\n")