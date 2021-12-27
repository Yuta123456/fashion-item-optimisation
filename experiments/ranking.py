import datetime
import itertools
import sys
import time
import gc
sys.path.append("D:\\fashion\\optimisation\\")
from util.save_closet import save_closet

from util_class.score_estimater import ScoreEstimater
from constants.optimisation import LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_all_item import init_all_item 
import tomotopy as tp
all_items = init_all_item(LAYER, LAYER_NAME, 8)
RANKING_NUM = 10

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
estimater = ScoreEstimater(topic_model, all_items)
"""
c, v, s, mをそれぞれbitに変換してそれを配列のindexにしている。
ex: 1101 -> s落とし
ex: 0111 -> c落とし
"""
ranking = [[-1 for i in range(RANKING_NUM)] for j in range(2**4)]
closet_ranking = [[None for i in range(RANKING_NUM)] for j in range(2**4)]

def update_ranking(score, score_ranking, c_closet, closet_ranking):
    for i in range(RANKING_NUM):
        if score > score_ranking[i]:
            score_ranking = score_ranking[:i] + [score] + score_ranking[i:-1]
            closet_ranking = closet_ranking[:i] + [c_closet] + closet_ranking[i:-1]
            break
    return (score_ranking, closet_ranking)
top_item_pick_array = list(itertools.combinations(all_items[0], TIME_STEP))
pants_item_pick_array = list(itertools.combinations(all_items[1], TIME_STEP))
shoes_item_pick_array = list(itertools.combinations(all_items[2], TIME_STEP))
all_count = len(top_item_pick_array) * len(pants_item_pick_array) * len(shoes_item_pick_array)
count = 0
flag = False
start_time = time.time()
for top_item_pick in top_item_pick_array:
    for pants_item_pick in pants_item_pick_array:
        gc.collect()
        for shoes_item_pick in shoes_item_pick_array:
            closet = [top_item_pick, pants_item_pick, shoes_item_pick]
            c, v, s, m = calc_closet_score(closet, estimater)
            for index in range(1, 2**4):
                bit_str = format(index, 'b').zfill(4)
                score = sum([s if bit_str[i] == '1' else 0 for i, s in enumerate([c, v, s, m])])
                ranking[index] ,closet_ranking[index] = update_ranking(score, ranking[index], closet, closet_ranking[index])
            count += 1
            if count % 1000 == 0:
                now = time.time()
                print(f"finish coodinate : {count * 100 / all_count} % { datetime.datetime.now()}")
                time_to_finish = now - start_time
                time_for_one = time_to_finish / count
                amount_time = (all_count - count) * time_for_one / 3600
                print("残り約{:.1f}時間です".format(amount_time))
                pre_time = now
for i in range(1, 16):
    print(f"====================={i}=======================")
    for j in range(RANKING_NUM):
        save_closet(closet_ranking[i][j], f"ranking/{i}/closet{j+1}")
        c, v, s, m = calc_closet_score(closet_ranking[i][j], estimater)
        bit_str = format(i, 'b').zfill(4)
        score = sum([s if bit_str[i] == '1' else 0 for i, s in enumerate([c, v, s, m])])
        print(score)

