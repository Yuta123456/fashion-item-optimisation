import glob

from util.calc_closet_score import calc_closet_score
from util.init_estimater import init_estimater
from util.load_closet import load_closet
closet_names = ["men/drop_cv", "men/drop_m", "men/drop_s", "men/full", "men/random", "men/drop_sm"]
estimater = init_estimater()

for name in closet_names:
    closet = load_closet(name)
    print(name)
    print("{} & {} & {} & {}".format(*calc_closet_score(closet, estimater)))