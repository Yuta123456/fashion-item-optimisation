import itertools
from constants.optimisation import TIME_STEP, WEIGHT
import numpy as np
from util.calc_coodinates_score import calc_coodinates_score
from util.standardization_score import standardization_score

from util_class.score_estimater import ScoreEstimater

def calc_closet_score(select_items, estimater: ScoreEstimater, raw = False):
    closet_score = np.array([0, 0, 0, 0], dtype=np.float64)
    for i in range(TIME_STEP):
        closet_score += np.array(calc_coodinates_score(select_items, select_items[2][i], 2, estimater, raw = raw), dtype=np.float64)
    closet_score = closet_score.tolist()
    sim_score = estimater.estimate_closet_similarity_score(select_items)
    closet_score[1] = sim_score
    return closet_score
    
