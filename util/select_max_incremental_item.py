from PIL import Image
import numpy as np
import tomotopy as tp
import itertools
from constants.optimisation import MEAN, STD, WEIGHT
from util.calc_coodinates_score import calc_coodinates_score
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
    max_score = [-1]
    for item in all_items[layer]:
        if any([item.get_id() == select_item.get_id() for select_item in select_items[layer]]):
            continue
        score_of_item = calc_coodinates_score(select_items, item, layer, estimater)
        if  sum(score_of_item) > sum(max_score):
            max_score = score_of_item
            max_incremental_item = item
    return (max_score, max_incremental_item)

