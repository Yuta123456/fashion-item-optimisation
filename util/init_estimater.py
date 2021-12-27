from constants.optimisation import LAYER, LAYER_NAME
from util.init_all_item import init_all_item
import tomotopy as tp

from util_class.score_estimater import ScoreEstimater

def init_estimater():
    all_items = init_all_item(LAYER, LAYER_NAME, 400)

    # FashionItemの初期化

    topic_model = tp.LDAModel.load('lda_model_topic_10.bin')

    return ScoreEstimater(topic_model, all_items)