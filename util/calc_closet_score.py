import itertools
from constants.optimisation import WEIGHT

from util_class.score_estimater import ScoreEstimater

def calc_closet_score(select_items, estimater: ScoreEstimater):
    k = [list(range(len(x))) for x in select_items]
    coodinates = []
    itertor = itertools.product(*k)
    for selected_num_array in itertor:
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            coodinate.append(select_items[i][selected_num])
        coodinates.append(coodinate)
    compatibility_score = estimater.estimate_compatibility_score(coodinates) * WEIGHT["com"]
    versatility_score = estimater.estimate_versatility_score(coodinates) * WEIGHT["ver"]
    simirality_score = estimater.estimate_closet_similarity_score(select_items) * WEIGHT["sim"]
    multiply_score = estimater.calc_multiplicity(coodinates) * WEIGHT["mul"]

    return [compatibility_score, versatility_score, simirality_score, multiply_score]
