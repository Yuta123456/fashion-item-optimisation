import datetime
import itertools
from os import close
import sys

sys.path.append("D:\\fashion\\optimisation\\")
from util.save_closet import save_closet

from util_class.score_estimater import ScoreEstimater
from constants.optimisation import LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_all_item import init_all_item 
import tomotopy as tp
all_items = init_all_item(LAYER, LAYER_NAME, 20)

RANKING_NUM = 10

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
estimater = ScoreEstimater(topic_model, all_items)
compatibility_ranking = [0 for i in range(RANKING_NUM)]
versatility_ranking =  [0 for i in range(RANKING_NUM)]
simirality_ranking = [0 for i in range(RANKING_NUM)]
multiply_ranking = [0 for i in range(RANKING_NUM)]
compatibility_closet_ranking = []
versatility_closet_ranking =  []
simirality_closet_ranking = []
multiply_closet_ranking = []

# TODO: 破壊的な変更なのでマジでごみ、許して
def update_ranking(score, score_ranking, c_closet, closet_ranking):
    for i in range(RANKING_NUM):
        if score > score_ranking[i]:
            score_ranking = score_ranking[:i] + [score] + score_ranking[i:-1]
            closet_ranking = closet_ranking[:i] + [c_closet] + closet_ranking[i:-1]
top_item_pick_array = list(itertools.combinations(all_items[0], TIME_STEP))
pants_item_pick_array = list(itertools.combinations(all_items[1], TIME_STEP))
shoes_item_pick_array = list(itertools.combinations(all_items[2], TIME_STEP))
print(len(top_item_pick_array),len(pants_item_pick_array), len(shoes_item_pick_array))
all_count = len(top_item_pick_array) * len(pants_item_pick_array) * len(shoes_item_pick_array)
count = 0
for top_item_pick in top_item_pick_array:
    for pants_item_pick in pants_item_pick_array:
        for shoes_item_pick in shoes_item_pick_array:
            closet = [top_item_pick, pants_item_pick, shoes_item_pick]
            c, v, s, m = calc_closet_score(closet, estimater)
            # print(c, v, s, m)
            update_ranking(c, compatibility_ranking, closet, compatibility_closet_ranking)
            update_ranking(v, versatility_ranking, closet, versatility_closet_ranking)
            update_ranking(s, simirality_ranking, closet, simirality_closet_ranking)
            update_ranking(m, multiply_ranking, closet, multiply_closet_ranking)
            count += 1
            if count % 1000 == 0:
                print(f"finish coodinate : {count * 100 / all_count} % {datetime.datetime.now()}")

# print(compatibility_ranking)
for i in range(RANKING_NUM):
    save_closet(compatibility_closet_ranking[i], f"com_ranking_{i+1}")
    save_closet(versatility_closet_ranking[i], f"ver_ranking_{i+1}")
    save_closet(simirality_closet_ranking[i], f"sim_ranking_{i+1}")
    save_closet(multiply_closet_ranking[i], f"mul_ranking_{i+1}")