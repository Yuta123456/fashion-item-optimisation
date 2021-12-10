import itertools
import copy

def make_coodinates(select_items, item, layer):
    coodinates = []
    select_items = copy.deepcopy(select_items)
    select_items[layer] = [item]
    k = [list(range(len(x))) for x in select_items]
    for selected_num_array in itertools.product(*k):
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            coodinate.append(select_items[i][selected_num])
        coodinates.append(coodinate)
    return coodinates