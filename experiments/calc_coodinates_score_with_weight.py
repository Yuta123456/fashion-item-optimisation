from util.make_coodinates import make_coodinates
from util.standardization_score import standardization_score
from util_class.score_estimater import ScoreEstimater


def calc_coodinates_score(select_items, item, layer,estimater: ScoreEstimater, weight):
    coodinates = make_coodinates(select_items, item, layer)

    compatibility_score = estimater.estimate_compatibility_score(coodinates)
    versatility_score = estimater.estimate_versatility_score(coodinates)
    simirality_score = estimater.estimate_similarity_score(item, select_items, layer)
    multiply_score = estimater.calc_multiplicity(coodinates)
    compatibility_score, versatility_score, simirality_score, multiply_score = \
    standardization_score(compatibility_score, versatility_score, simirality_score, multiply_score)
    score_of_item = max(0, compatibility_score) * weight["com"], \
                    max(0, versatility_score)   * weight["ver"], \
                    max(0, simirality_score)    * weight["sim"], \
                    max(0, multiply_score)      * weight["mul"]
    return score_of_item