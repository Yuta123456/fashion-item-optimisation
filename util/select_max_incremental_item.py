from PIL import Image
import numpy as np
import tomotopy as tp
import itertools
from constants.optimisation import MEAN, STD, WEIGHT
from util.make_coodinates import make_coodinates
from util.record_data import record_data
from util.standardization_score import standardization_score
from util_class.score_estimater import ScoreEstimater
# スコアを計算するクラスを作れば、モデルを受け渡しする必要がなくなる。

"""
一番評価指標が多いアイテムを選ぶ
一つ一つのアイテムはFashionItemの方に従う
"""
def select_max_incremental_item(select_items, all_items, layer, estimater: ScoreEstimater):
    # LAYERのアイテムに対して回す
    max_incremental_item = None
    max_score = -1
    for item in all_items[layer]:
        # print(item, select_items)
        if any([item.get_id() == select_item.get_id() for select_item in select_items[layer]]):
            continue
        coodinates = []
        coodinates = make_coodinates(select_items, item, layer)
        compatibility_score = estimater.estimate_compatibility_score(coodinates)
        versatility_score = estimater.estimate_versatility_score(coodinates)
        simirality_score = estimater.estimate_similarity_score(item, select_items, layer)
        multiply_score = estimater.calc_multiplicity(coodinates)
        compatibility_score, versatility_score, simirality_score, multiply_score = \
        standardization_score(compatibility_score, versatility_score, simirality_score, multiply_score)

        score_of_item = max(0, compatibility_score) * WEIGHT["com"] \
                      + max(0, versatility_score)   * WEIGHT["ver"] \
                      + max(0, simirality_score)    * WEIGHT["sim"] \
                      + max(0, multiply_score)      * WEIGHT["mul"]
        if  score_of_item > max_score:
            max_score =  score_of_item
            max_incremental_item = item
    return (max_score, max_incremental_item)

