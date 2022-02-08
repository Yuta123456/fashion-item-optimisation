import itertools
import copy

from constants.optimisation import LAYER

def make_coodinates(select_items, item, layer):
    coodinates = []
    select_items_copy = copy.deepcopy(select_items)
    select_items_copy[layer] = [item]
    k = [list(range(len(x))) for x in select_items_copy]
    for selected_num_array in itertools.product(*k):
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            coodinate.append(select_items_copy[i][selected_num])
        if len(coodinate) == LAYER:
            coodinates.append(coodinate)
    return coodinates


def make_all_coodinates(select_items):
    coodinates = []
    k = [list(range(len(x))) for x in select_items]
    for selected_num_array in itertools.product(*k):
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            coodinate.append(select_items[i][selected_num])
        if len(coodinate) == LAYER:
            coodinates.append(coodinate)
    return coodinates


def make_lost_item_closet(closet, item_id):
    res_closet = [[] for i in range(LAYER)]
    for i in range(LAYER):
        for j in closet[i]:
            if j.get_id() != item_id:
                res_closet[i].append(j)
    return res_closet