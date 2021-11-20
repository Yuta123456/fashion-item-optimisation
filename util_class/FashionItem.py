from PIL import Image


class FashionItem:
    # instance variable
    image = None
    # 必要かどうか？
    layer = None
    # 属性を文字列の配列でもっておく
    attr = []
    # 一意に定まるID
    id = None
    # 画像へのパス
    image_path = None
    def __init__(self, image_path, layer, attr, id):
        # TODO: implement init process
        self.image_path = image_path
        self.layer = layer
        self.attr = attr
        self.id = id
        return
    
    def get_image(self):
        return Image.open(self.image_path)
    
    def get_layer(self):
        return self.layer

    def get_attr(self):
        return self.attr
    
    def get_id(self):
        return self.id