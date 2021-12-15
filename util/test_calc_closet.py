from constants.optimisation import LAYER, LAYER_NAME
from util.calc_closet_score import calc_closet_score
from util.init_all_item import init_all_item
from util.load_closet import load_closet
from util.save_closet import save_closet
from util.show_closet_info import show_closet_info
from util.show_fashion_images import show_fashion_images
from util_class.score_estimater import ScoreEstimater
import tomotopy as tp
all_items = init_all_item(LAYER, LAYER_NAME, 100)

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
estimater = ScoreEstimater(topic_model, all_items)
closet = load_closet("yuta_tanaka")
# print(closet)
show_fashion_images(closet)
print("com:{} ver:{} sim:{} mul:{} ".format(*calc_closet_score(closet, estimater)))