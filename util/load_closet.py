import os
import uuid

from matplotlib.pyplot import locator_params
from util_class.FashionItem import FashionItem
import re

def load_closet(filename, layer_num, layer_name):
    select_items = [[] for i in range(layer_num)]
    with open("data/" + filename, mode='r') as f:
        for line in f:
            line = line.strip()
            if os.path.exists(line):
                image_path = line
            else:
                continue
            local = re.findall(r'\\(top|pants|shoes)', image_path)[0]
            for i, name in enumerate(layer_name):
                if local == name:
                    layer = i
            id = uuid.uuid4()
            dir_path = re.sub(r'\\(top|pants|shoes).jpg', "/attribute2.txt", image_path)
            with open(dir_path) as f_a:
                # 該当するレイヤーのアイテムだけ取得
                attribute = [s.strip() for s in f_a.readlines() if s.startswith(local)]
                attribute = list(set(attribute))
            item = FashionItem(image_path, layer, attribute, id)
            select_items[layer].append(item)
    return select_items
# def init_all_item(LAYER, LAYER_NAME, length):
#     all_item = [[] for i in range(LAYER)]
#     dir_pathes = glob.glob('../images/RichWearImageSprited/**/**/')[:length]
#     for dir_path in dir_pathes:
#         for layer in range(LAYER):
#             layer_name = LAYER_NAME[layer]
#             image_path = dir_path + f"{layer_name}.jpg"
#             if os.path.exists(image_path):
#                 image_path = dir_path + f"{layer_name}.jpg"
#             else:
#                 continue
#             with open(dir_path + "attribute.txt") as f:
#                 # 該当するレイヤーのアイテムだけ取得
#                 attribute = [s.strip() for s in f.readlines() if s.startswith(layer_name)]
#                 attribute = list(set(attribute))
#             id = uuid.uuid4()
#             if len(attribute) == 0:
#                 continue
#             item = FashionItem(image_path, layer, attribute, id)
#             all_item[layer].append(item)
#     return all_item

# ../images/RichWearImageSprited\1-1\20170324100637269_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324102130173_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324103028833_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324101830592_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324095351514_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324095648905_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324101509945_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324100701593_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324093844249_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324095254453_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324100218685_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324100303683_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324101511276_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324095307198_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324095603406_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324101213515_500\top.jpg
# ../images/RichWearImageSprited\1-1\20170324103244682_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324100701593_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324095648905_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324101509945_500\pants.jpg
# ../images/RichWearImageSprited\1-1\20170324102806575_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324100218685_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324095254453_500\shoes.jpg
# ../images/RichWearImageSprited\1-1\20170324100303683_500\shoes.jpg
