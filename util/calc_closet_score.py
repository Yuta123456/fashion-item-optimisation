import itertools

from util_class.score_estimater import ScoreEstimater


def calc_closet_score(select_items, estimater: ScoreEstimater):
    k = [list(range(len(x))) for x in select_items]
    coodinates = []
    for selected_num_array in itertools.product(*k):
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            coodinate.append(select_items[i][selected_num])
        coodinates.append(coodinate)
    compatibility_score = estimater.estimate_compatibility_score(coodinates)
    versatility_score = estimater.estimate_versatility_score(coodinates)
    simirality_score = 0
    for layer in range(len(select_items)):
        for item in select_items[layer]:
            simirality_score += estimater.estimate_similarity_score(item, select_items, layer)
    multiply_score = estimater.calc_multiplicity(coodinates)
    return (compatibility_score, versatility_score, simirality_score, multiply_score)
