from PIL import Image
import numpy as np
import os
import sys
import glob
import tomotopy as tp
import itertools
from util.make_coodinates import make_coodinates
# スコアを計算するクラスを作れば、モデルを受け渡しする必要がなくなる。
"""
一番評価指標が多いアイテムを選ぶ
一つ一つのアイテムはFashionItemの方に従う
"""
def select_max_incremental_item(select_items, all_items, layer, estimater):
    # LAYERのアイテムに対して回す
    max_incremental_item = None
    max_score = -1
    for item in all_items[layer]:
        coodinates = []
        coodinates = make_coodinates(select_items, item, layer)
        compatibility_score = estimater.estimate_compatibility_score(coodinates)
        versatility_score = estimater.estimate_versatility_score(coodinates)
        simirality_score = estimater.estimate_similarity_score(item, select_items, layer)
        print("com:{} ver:{} sim:{}".format(compatibility_score, versatility_score, simirality_score))
        score_of_item = compatibility_score + versatility_score + simirality_score
        if  score_of_item > max_score:
            max_score =  score_of_item
            max_incremental_item = item
    return (max_score, max_incremental_item)

