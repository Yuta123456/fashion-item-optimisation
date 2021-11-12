import itertools


def make_coodinates(select_items, item, layer):
    coodinates = []
    k = [list(range(len(x))) for x in select_items]
    for selected_num_array in itertools.product(*k):
        coodinate = []
        for i, selected_num in enumerate(selected_num_array):
            if i == layer:
                coodinate.append(item)
                continue
            coodinate.append(select_items[i][selected_num])
        coodinates.append(coodinate)
    return coodinates