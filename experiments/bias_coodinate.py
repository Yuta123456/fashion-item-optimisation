import sys
import glob
sys.path.append("D:\\fashion\\optimisation\\")

from constants.optimisation import LAYER, SIGMA_B
from util.init_estimater import init_estimater
from util.load_closet import load_closet
from util.make_coodinates import make_all_coodinates, make_coodinates, make_lost_item_closet

closet_path_list = glob.glob("./closet/men/**")
closet_path_list = list(map(lambda x: x.replace("./closet/",""), closet_path_list))
print(closet_path_list)
model = init_estimater()

for path in closet_path_list:
    score = 0
    closet = load_closet(path)
    for layer in range(LAYER):
        for item in closet[layer]:
            coodinates_lost = make_coodinates(closet, item, layer)
            score = max(score, sum(map(lambda x : int(model.estimate_coodinate_compatibility(x) > SIGMA_B), coodinates_lost)))
    coodinates = make_all_coodinates(closet)
    coodinate_num = model.calc_multiplicity(coodinates)
    print(f"Score:{path}, {score}, {coodinate_num}")
