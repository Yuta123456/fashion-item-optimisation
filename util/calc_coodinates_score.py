from constants.optimisation import WEIGHT
from util.make_coodinates import make_coodinates
from util.record_data import record_data
from util.standardization_score import standardization_score
from util_class.score_estimater import ScoreEstimater


def calc_coodinates_score(select_items, item, layer,estimater: ScoreEstimater, raw = False):
    coodinates = make_coodinates(select_items, item, layer)

    compatibility_score = estimater.estimate_compatibility_score(coodinates)
    versatility_score = estimater.estimate_versatility_score(coodinates)
    simirality_score = estimater.estimate_similarity_score(item, select_items, layer)
    multiply_score = estimater.calc_multiplicity(coodinates)
    if raw:
        return (compatibility_score, versatility_score, simirality_score, multiply_score)
    compatibility_score, versatility_score, simirality_score, multiply_score = \
    standardization_score(compatibility_score, versatility_score, simirality_score, multiply_score)
    score_of_item = max(0, compatibility_score) * WEIGHT["com"], \
                    max(0, versatility_score)   * WEIGHT["ver"], \
                    max(0, simirality_score)    * WEIGHT["sim"], \
                    max(0, multiply_score)      * WEIGHT["mul"]
    record_data("data/rand_com.txt", score_of_item[0])
    record_data("data/rand_ver.txt", score_of_item[1])
    record_data("data/rand_sim.txt", score_of_item[2])
    record_data("data/rand_mul.txt", score_of_item[3])
    return score_of_item