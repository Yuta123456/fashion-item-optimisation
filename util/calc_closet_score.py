from constants.optimisation import MEAN, STD, TIME_STEP, WEIGHT2
import numpy as np
from util.calc_coodinates_score import calc_coodinates_score
from util.record_data import record_data

from util_class.score_estimater import ScoreEstimater

def calc_closet_score(select_items, estimater: ScoreEstimater, raw = False):
    closet_score = np.array([0, 0, 0, 0], dtype=np.float64)
    for i in range(TIME_STEP):
        closet_score += np.array(calc_coodinates_score(select_items, select_items[2][i], 2, estimater), dtype=np.float64)
    closet_score = closet_score.tolist()
    sim_score = estimater.estimate_closet_similarity_score(select_items)
    # print(sim_score)
    sim_score = sum(list(map(lambda x: max(0, (x - MEAN["sim"]) / STD["sim"]), sim_score))) * WEIGHT2["sim"]
    closet_score[2] = sim_score
    return closet_score
    
