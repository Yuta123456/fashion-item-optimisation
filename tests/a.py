import unittest
import sys

import numpy as np
sys.path.append("D:\\fashion\\optimisation\\")
from constants.optimisation import LAYER, LAYER_NAME, TIME_STEP, WEIGHT
from util.calc_closet_score import calc_closet_score

from util.init_all_item import init_all_item
from util.init_closet import init_closet
from util.make_coodinates import make_coodinates
import tomotopy as tp
import torch
from torchvision import models
import torch.nn as nn
from util.standardization_score import standardization_score
from util_class.score_estimater import ScoreEstimater
class TestUnilFunctions(unittest.TestCase):

    def setUp(self):
        all_items = init_all_item(LAYER, LAYER_NAME, 100)
        topic_model = tp.LDAModel.load('lda_model_topic_10.bin')
        similarity_model = models.resnet18(pretrained=True)
        num_ftrs = similarity_model.fc.in_features

        similarity_model.fc = nn.Linear(num_ftrs,  738)
        similarity_model.load_state_dict(torch.load('model.pth'))
        model = ScoreEstimater(topic_model, all_items, similarity_model)
        self.model = model
        self.all_items = all_items

    def test_make_coodinates(self):
        select_items = [["one", "two"], ["three"], ["four", "five", "six"]]
        item = "seven"
        layer = 2
        make_coodinates(select_items, item, layer)

    def test_calc_closet_score(self):
        closet = init_closet(self.all_items, 4)
        score_a = calc_closet_score(closet, self.model)
        score_b = np.array([0, 0, 0, 0], dtype=np.float64)
        for i in range(TIME_STEP):
            score_b += np.array(self.calc_score_add_item(closet, closet[2][i]), dtype=np.float64)
        score_b = score_b.tolist()
        score_c = calc_closet_score(closet, self.model)
        self.assertEqual(score_a, score_c)
        self.assertEqual(score_a, score_b)

    def calc_score_add_item(self, select_items, item):
        coodinates = make_coodinates(select_items, item, 2)

        compatibility_score = self.model.estimate_compatibility_score(coodinates)
        versatility_score = self.model.estimate_versatility_score(coodinates)
        simirality_score = self.model.estimate_similarity_score(item, select_items, 2)
        multiply_score = self.model.calc_multiplicity(coodinates)
        compatibility_score, versatility_score, simirality_score, multiply_score = \
        standardization_score(compatibility_score, versatility_score, simirality_score, multiply_score)

        score_of_item = max(0, compatibility_score) * WEIGHT["com"],\
                        max(0, versatility_score)   * WEIGHT["ver"],\
                        max(0, simirality_score)    * WEIGHT["sim"], \
                        max(0, multiply_score)      * WEIGHT["mul"]
        return score_of_item
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()