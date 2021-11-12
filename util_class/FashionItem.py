class FashionItem:
    # instance variable
    image = None
    # 必要かどうか？
    layer = None
    # 属性を文字列の配列でもっておく
    attr = []
    # 一意に定まるID
    id = None
    def __init__(self, image, layer, attr, id):
        # TODO: implement init process
        self.image = image
        self.layer = layer
        self.attr = attr
        self.id = id
        return
    
    def get_image(self):
        return self.image
    
    def get_layer(self):
        return self.layer

    def get_attr(self):
        return self.attr
    
    def get_id(self):
        return self.id