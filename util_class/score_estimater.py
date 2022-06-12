from constants.optimisation import LAYER, SIMILARITY_THRESHOLD

from util.image_similarity_measures import rmse
import numpy as np
import math
from torchvision import transforms
from torchvision.models.feature_extraction import create_feature_extractor
import torch
from util.record_data import record_data
class ScoreEstimater:
    # instance variable
    topic_model = None
    similarity_model = None
    all_items = None
    similarity_cache = {}
    transform  = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)

    def __init__(self, topic_model, all_items, similarity_model):
        # TODO: implement init process
        self.topic_model = topic_model
        self.all_items = all_items

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        m = similarity_model.to(self.device)
        feature_extractor = create_feature_extractor(m, {"avgpool": "feature"})
        self.similarity_model = feature_extractor
    
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
        return ver_score / (topic_num * coodinate_len)

    def estimate_similarity_score(self, fashion_item, select_items,layer):
        covering_item_ids = set()
        covering_item_cnt = 0
        for item in self.all_items[layer]:
            for select_item in select_items[layer]:
                # もし類似度計算をして、閾値より低ければカバーしたと断定。
                if item.get_id() not in covering_item_ids and self.calc_image_similarity(item, select_item) < SIMILARITY_THRESHOLD : 
                    covering_item_ids.add(item.get_id())
                    break
        
        for item in self.all_items[layer]:
            # 新しく追加されたアイテムと類似度計算をして、閾値より低ければ、新しくカバーしたと断定。
            if self.calc_image_similarity(item, fashion_item) < SIMILARITY_THRESHOLD and item.get_id() not in covering_item_ids:
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
        image_a = item_a.get_image()
        image_b = item_b.get_image()
        image_a = torch.tensor(self.transform(image_a))
        image_b = torch.tensor(self.transform(image_b))
        image_a = image_a.unsqueeze(0).to(self.device)
        image_b = image_b.unsqueeze(0).to(self.device)

        image_a_vec = self.similarity_model(image_a)["feature"].flatten()
        image_b_vec = self.similarity_model(image_b)["feature"].flatten()
        dist = self.cos(image_a_vec, image_b_vec)
        return dist

    
    """
    洋服の重複度
    """
    def calc_multiplicity(self, coodinates):
        com_good_count = 0
        threshold = 7
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            doc = []
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
        
        return result
    
    def estimate_closet_similarity_score(self,select_items):       
        covering_item_ids = set()
        for layer in range(LAYER):
            for item in self.all_items[layer]:
                for select_item in select_items[layer]:
                    # もし類似度計算をして、閾値より低ければカバーしたと断定。
                    score = self.calc_image_similarity(item, select_item).item()
                    record_data("./data/sim_new.txt", score)
                    if score < SIMILARITY_THRESHOLD:
                        covering_item_ids.add(item.get_id())
                        break
        return len(covering_item_ids)