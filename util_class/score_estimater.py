from constants.optimisation import LAYER, SIGMA_B, SIMILARITY_THRESHOLD, TIME_STEP

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
    features_cache = {}
    transform  = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    # ユークリッド距離を計算
    calc_dist = torch.nn.PairwiseDistance(p=2)

    def __init__(self, topic_model, all_items, similarity_model):
        self.topic_model = topic_model
        self.all_items = all_items
        self.all_item_num = sum([len(i) for i in self.all_items])
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        m = similarity_model.to(self.device)
        feature_extractor = create_feature_extractor(m, {"avgpool": "feature"})
        self.similarity_model = feature_extractor
    
    def set_all_items(self, all_items):
        self.all_items = all_items
        self.all_item_num = sum([len(i) for i in self.all_items])

    def estimate_compatibility_score(self, coodinates):
        com_score = 0
        # coodinateは、FashionItemの配列
        assert(coodinates <= 16)
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
        assert(coodinate_len <= 16)
        # topic数で正規化。0-1の範囲に収まる
        return ver_score / (topic_num * coodinate_len)

    def estimate_similarity_score(self, fashion_item, select_items, layer):
        covering_item_ids = set()
        covering_item_cnt = 0
        # ここめちゃくちゃおっそい。
        for item in self.all_items[layer]:
            for select_item in select_items[layer]:
                # もし類似度計算をして、閾値より低ければカバーしたと断定。
                if self.calc_image_similarity(item, select_item) < SIMILARITY_THRESHOLD:
                    covering_item_ids.add(item.get_id())
                    break
        
        for item in self.all_items[layer]:
            if item.get_id() not in covering_item_ids:
                # もし、既にカバーされてるんだったら、新しくないのでスキップ
                continue
            # 新しく追加されたアイテムと類似度計算をして、閾値より低ければ、新しくカバーしたと断定。
            if self.calc_image_similarity(item, fashion_item) < SIMILARITY_THRESHOLD:
                covering_item_ids.add(item.get_id())
                covering_item_cnt += 1

        return covering_item_cnt / len(self.all_items[0])
    
    def calc_image_similarity(self, item_a, item_b):
        image_a_vec = self.calc_image_feature(item_a)
        image_b_vec = self.calc_image_feature(item_b)
        dist = self.calc_dist(image_a_vec, image_b_vec)
        dist = dist.item()
        return dist

    """
    洋服の特徴量を計算する
    """
    def calc_image_feature(self, item):
        item_id = item.get_id()
        if item_id in self.features_cache:
            return self.features_cache[item_id]
        image = item.get_image()
        image = self.transform(image)
        image = image.unsqueeze(0).to(self.device)
        image_feature = self.similarity_model(image)["feature"].flatten().detach().cpu()
        self.features_cache[item_id] = image_feature
        return image_feature
    """
    洋服の重複度
    """
    def calc_multiplicity(self, coodinates):
        com_good_count = 0
        # coodinateは、FashionItemの配列
        for coodinate in coodinates:
            com_score = self.estimate_coodinate_compatibility(coodinate)
            if com_score > SIGMA_B:
                com_good_count += 1
        assert(com_good_count <= 16)
        return com_good_count / 16

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

        return result
    
    def estimate_closet_similarity_score(self, select_items):
        covering_item_ids = set()
        for layer in range(LAYER):
            for item in self.all_items[layer]:
                for select_item in select_items[layer]:
                    # もし類似度計算をして、閾値より低ければカバーしたと断定。
                    score = self.calc_image_similarity(item, select_item)
                    if score < SIMILARITY_THRESHOLD:
                        covering_item_ids.add(item.get_id())
                        break

        return len(covering_item_ids) / len(self.all_items[0])
