from constants.optimisation import LAYER, LAYER_NAME


def show_closet_info(select_items):
    for layer in range(LAYER):
        print(f"layer{layer}, name: {LAYER_NAME[layer]}")
        for item in select_items[layer]:
            print(f"path: {item.get_image_path()} attributes: {item.get_attr()}")  
    