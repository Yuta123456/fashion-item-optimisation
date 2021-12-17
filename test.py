import glob
from constants.optimisation import LAYER, LAYER_NAME, TIME_STEP
from util.init_all_item import init_all_item 
from util.init_closet  import init_closet
from util.save_closet import save_closet
all_items = init_all_item(LAYER, LAYER_NAME, 180)
closet = init_closet(all_items, TIME_STEP)
save_closet(closet, "women/random")