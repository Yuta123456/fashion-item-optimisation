def show_fashion_images(select_items):
    for layer, items_in_layer in enumerate(select_items):
        print(f"layer : {layer}")
        for items in items_in_layer:
            image = items.get_image()
            # 改良の余地あり、おそらく枚数分出てきてめんどくさい。
            image.show()

