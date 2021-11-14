
from util.image_similarity_measures import rmse
from PIL import Image
import numpy as np
import math
class ScoreEstimater:
    # instance variable
    topic_model = None
    all_items = None
    def __init__(self, topic_model, all_items):
        # TODO: implement init process
        self.topic_model = topic_model
        self.all_items = all_items
    
    def estimate_compatibility_score(self, coodinates):
        com_score = 0
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            doc = []
            for item in coodinate:
                doc += item.get_attr()
                try:
                    inf_doc = self.topic_model.make_doc(doc)
                except:
                    print(doc, item.get_attr(), )
                result = self.topic_model.infer(inf_doc)
                # 対数であったり、問題はありそう。
                result = result[1]
                com_score += math.pow(math.e, result)
        return com_score

    def estimate_versatility_score(self, coodinates): 
        ver_score = 0
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            doc = []
            ver = 1
            for item in coodinate:
                doc += item.get_attr()
            inf_doc = self.topic_model.make_doc(doc)
            result = self.topic_model.infer(inf_doc)
            topic_prob = result[0]
            for topic in topic_prob:
                ver *= (1 - topic)
            ver_score += (1 - ver)
        return ver_score

    def estimate_similarity_score(self, fashion_item, select_items,layer):
        # 今の閾値は適当
        threshold = 0.015
        covering_item_ids = set()
        covering_item_cnt = 0
        for item in self.all_items[layer]:
            for select_item in select_items[layer]:
                # もし類似度計算をして、閾値より低ければカバーしたと断定。
                if self.calc_image_similarity(item, select_item) < threshold and item.get_id() not in covering_item_ids : 
                    covering_item_ids.add(item.get_id())
                    break
        
        for item in self.all_items[layer]:
            # 新しく追加されたアイテムと類似度計算をして、閾値より低ければ、新しくカバーしたと断定。
            if self.calc_image_similarity(item, fashion_item) < threshold and item.get_id() not in covering_item_ids: 
                covering_item_ids.add(item.get_id())
                covering_item_cnt += 1
        return covering_item_cnt

    def calc_image_similarity(self, item_a, item_b):
        image_a = np.array(item_a.get_image())
        # image1のサイズ取得
        image_a_shape = image_a.shape
        # Resize処理をかける
        image_b = np.array(item_b.get_image())
        image_b.resize(image_a_shape)

        # 距離計算
        result = rmse(image_a, image_b)
        return result