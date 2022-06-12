# レイヤーの個数 ex) tops, pants, shoes -> LAYER = 3
import random
import sys
import time
from constants.optimisation import EPSILON, LAYER, LAYER_NAME, TIME_STEP
from util.calc_closet_score import calc_closet_score
from util_class.score_estimater import ScoreEstimater

import tomotopy as tp
from util.init_all_item import init_all_item
from util.record_data import record_data

import torch
import torch.nn as nn
from torchvision import models, transforms
start = time.time()
all_items = init_all_item(LAYER, LAYER_NAME, 400)

# FashionItemの初期化

topic_model = tp.LDAModel.load('lda_model_topic_10.bin')

similarity_model = models.resnet18(pretrained=True)
num_ftrs = similarity_model.fc.in_features

similarity_model.fc = nn.Linear(num_ftrs,  738)

similarity_model.load_state_dict(torch.load('model.pth'))

if "--clear" in sys.argv:
    with open("data/com.txt", mode="w") as f:
        f.write("")
    with open("data/sim.txt", mode="w") as f:
        f.write("")
    with open("data/ver.txt", mode="w") as f:
        f.write("")
    with open("data/mul.txt", mode="w") as f:
        f.write("")
    print("data clear run")
estimater = ScoreEstimater(topic_model, all_items, similarity_model)
COUNT = 20000
for c in range(COUNT):
    closet = []
    for i in range(LAYER):
        closet.append(random.sample(all_items[i], 4))
    score = calc_closet_score(closet, estimater)
    record_data("data/com.txt", score[0])
    record_data("data/ver.txt", score[1])
    record_data("data/sim.txt", score[2])
    record_data("data/mul.txt", score[3])
    if c % 1000 == 0:
        print(f"{c * 100 / COUNT}%")