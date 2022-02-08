import os
import uuid

from matplotlib.pyplot import locator_params
from constants.optimisation import LAYER, LAYER_NAME

from util_class.FashionItem import FashionItem
import re

def load_closet(filename):
    select_items = [[] for i in range(LAYER)]
    with open("closet/" + filename, mode='r') as f:
        for line in f:
            line = line.strip()
            if os.path.exists(line):
                image_path = line
            else:
                continue
            local = re.findall(r'\\(top|pants|shoes)', image_path)[0]
            for i, name in enumerate(LAYER_NAME):
                if local == name:
                    layer = i
            id = uuid.uuid4()
            dir_path = re.sub(r'\\(top|pants|shoes).jpg', "/attribute2.txt", image_path)
            with open(dir_path) as f_a:
                # 該当するレイヤーのアイテムだけ取得
                attribute = [s.strip() for s in f_a.readlines() if s.startswith(local)]
                attribute = list(set(attribute))
            # print(f"{layer} {attribute}")
            item = FashionItem(image_path, layer, attribute, id)
            select_items[layer].append(item)
    # print(select_items)
    return select_items
