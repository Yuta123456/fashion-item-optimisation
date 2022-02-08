

from cv2 import threshold
from constants.optimisation import LAYER, SIGMA_B
from util.image_similarity_measures import rmse
import numpy as np
import math
class ScoreEstimater:
    # instance variable
    topic_model = None
    all_items = None
    similarity_cache = {}
    def __init__(self, topic_model, all_items):
        # TODO: implement init process
        self.topic_model = topic_model
        self.all_items = all_items
    
    def estimate_compatibility_score(self, coodinates):
        com_score = 0
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            com_score += self.estimate_coodinate_compatibility(coodinate)
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
        topic_num = self.topic_model.k
        coodinate_len = len(coodinates)
        if (topic_num * coodinate_len) == 0:
            return ver_score
        # topic数で正規化。0-1の範囲に収まる
        del doc
        del inf_doc
        del result  
        del topic_prob
        return ver_score / (topic_num * coodinate_len)

    def estimate_similarity_score(self, fashion_item, select_items,layer):
        threshold = 0.025112
        covering_item_ids = set()
        covering_item_cnt = 0
        for item in self.all_items[layer]:
            for select_item in select_items[layer]:
                # もし類似度計算をして、閾値より低ければカバーしたと断定。
                if item.get_id() not in covering_item_ids and self.calc_image_similarity(item, select_item) < threshold : 
                    covering_item_ids.add(item.get_id())
                    break
        
        for item in self.all_items[layer]:
            # 新しく追加されたアイテムと類似度計算をして、閾値より低ければ、新しくカバーしたと断定。
            if self.calc_image_similarity(item, fashion_item) < threshold and item.get_id() not in covering_item_ids: 
                covering_item_ids.add(item.get_id())
                covering_item_cnt += 1
        # アイテム数で正規化
        all_item_cnt = len(self.all_items[layer])
        del covering_item_ids
        return covering_item_cnt / all_item_cnt

    def calc_image_similarity(self, item_a, item_b):
        key = (item_a.get_id(), item_b.get_id())
        if key in self.similarity_cache:
            return self.similarity_cache[key]
        image_a = np.array(item_a.get_image())
        # image1のサイズ取得
        image_a_shape = image_a.shape
        # Resize処理をかける
        image_b = np.array(item_b.get_image())
        # image_b.resize(image_a_shape)
        image_b = np.resize(image_b, image_a_shape)

        # 距離計算
        result = rmse(image_a, image_b)
        self.similarity_cache[key] = result
        # record_data("data/simirality.txt", str(result))
        del image_a
        del image_b
        del image_a_shape
        return result
    
    """
    洋服の重複度
    """
    def calc_multiplicity(self, coodinates):
        com_good_count = 0
        threshold = 7
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            doc = []
            for item in coodinate:
                doc += item.get_attr()
            com_score = self.estimate_coodinate_compatibility(coodinate)
            if com_score > threshold:
                com_good_count += 1
        del doc

        return com_good_count

    def estimate_coodinate_compatibility(self, coodinate):
        doc = []
        for item in coodinate:
            doc += item.get_attr()
        try:
            inf_doc = self.topic_model.make_doc(doc)
        except:
            print(doc)
        result = self.topic_model.infer(inf_doc)
        # 対数であったり、問題はありそう。
        result = result[1]
        result = math.pow(math.e, result)
        result = result * pow(10, 22)
        result = 0 if result < 1 else math.log(result)
        del doc
        del inf_doc
        return result
    
    def estimate_closet_similarity_score(self,select_items):       
        covering_item_ids = set()
        threshold = 0.025112
        for layer in range(LAYER):
            for item in self.all_items[layer]:
                for select_item in select_items[layer]:
                    # もし類似度計算をして、閾値より低ければカバーしたと断定。
                    if self.calc_image_similarity(item, select_item) < threshold : 
                        covering_item_ids.add(item.get_id())
                        break   
        return len(covering_item_ids)