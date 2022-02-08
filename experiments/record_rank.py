import datetime
import itertools
import sys
import time
import gc

sys.path.append("D:\\fashion\\optimisation\\")

from util_class.score_estimater import ScoreEstimater
from constants.optimisation import LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util.init_all_item import init_all_item 
import tomotopy as tp
from memory_profiler import profile
@profile
def main():
    all_items = init_all_item(LAYER, LAYER_NAME, 7)

    topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
    estimater = ScoreEstimater(topic_model, all_items)
    """
    c, v, s, mをそれぞれbitに変換してそれを配列のindexにしている。
    ex: 1101 -> s落とし
    ex: 0111 -> c落とし
    """
    # show_fashion_images(all_items)
    top_item_pick_array = list(itertools.combinations(all_items[0], TIME_STEP))
    pants_item_pick_array = list(itertools.combinations(all_items[1], TIME_STEP))
    shoes_item_pick_array = list(itertools.combinations(all_items[2], TIME_STEP))
    all_count = len(top_item_pick_array) * len(pants_item_pick_array) * len(shoes_item_pick_array)
    count = 0
    start_time = time.time()
    for top_item_pick in top_item_pick_array:
        for pants_item_pick in pants_item_pick_array:
            gc.collect()
            for shoes_item_pick in shoes_item_pick_array:
                closet = [top_item_pick, pants_item_pick, shoes_item_pick]
                c, v, s, m = calc_closet_score(closet, estimater)
                with open("data/ranking_data.txt", mode='a') as f:
                    f.write(f"{c} {v} {s} {m}\n")
                count += 1
                if count % 1000 == 0:
                    now = time.time()
                    print(f"finish coodinate : {count * 100 / all_count} % { datetime.datetime.now()}")
                    time_to_finish = now - start_time
                    time_for_one = time_to_finish / count
                    amount_time = (all_count - count) * time_for_one / 3600
                    print("残り約{:.1f}時間です".format(amount_time))
                    del time_to_finish
                    del time_for_one
                    del amount_time
                    del now
                del closet
                del c, s, v, m
                
                
if __name__ == "__main__":
    main()
#  1063.8 MiB