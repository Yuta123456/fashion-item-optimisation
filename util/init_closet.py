import random
from constants.optimisation import LAYER

def init_closet(all_items, time_step):
    closet = []
    for i in range(LAYER):
        # print(time_step, len(all_items[i]))
        closet.append(random.sample(all_items[i], time_step))
    return closet