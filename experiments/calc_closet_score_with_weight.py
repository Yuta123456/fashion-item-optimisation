from constants.optimisation import MEAN, STD, TIME_STEP
import numpy as np
from calc_coodinates_score_with_weight import calc_coodinates_score
from util.record_data import record_data

from util_class.score_estimater import ScoreEstimater

def calc_closet_score(select_items, estimater: ScoreEstimater, weight):
    closet_score = np.array([0, 0, 0, 0], dtype=np.float64)
    for i in range(TIME_STEP):
        closet_score += np.array(calc_coodinates_score(select_items, select_items[2][i], 2, estimater, weight), dtype=np.float64)
    closet_score = closet_score.tolist()
    sim_score = estimater.estimate_closet_similarity_score(select_items)
    sim_score = sum(list(map(lambda x: x - MEAN["sim"] / STD["sim"], sim_score))) * weight["sim"]
    # similarityだけ標準化できていない。
    closet_score[2] = sim_score
    return closet_score
    
