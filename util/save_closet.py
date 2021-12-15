from util_class.FashionItem import FashionItem


def save_closet(select_items, filename):
    for layer_item in select_items:
        for item in layer_item:
            with open("closet/" + filename, mode='a') as f:
                # 該当するレイヤーのアイテムだけ取得
                f.write(str(item.get_image_path()) + "\n")