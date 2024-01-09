import numpy as np
import pands as pd
import torch
import torch.nn as nn
from torchvision.models import resnet18


class ResNet18:
    WEIGHTS_PATH = "./weights/best.pt"

    CLASSES_KEY = {
        0: "plane",
        1: "car",
        2: "bird",
        3: "cat",
        4: "deer",
        5: "dog",
        6: "frog",
        7: "horse",
        8: "ship",
        9: "truck",
    }

    def __init__(self, weights_path=WEIGHTS_PATH, classes_key=CLASSES_KEY):
        self.model = resnet18()
        self.model.fc = nn.Sequential(
            nn.Linear(self.model.fc.in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 10),
            nn.LogSoftmax(dim=1),
        )
        self.model.load_state_dict(
            torch.load(
                weights_path,
                map_location="cuda:0" if torch.cuda.is_available() else "cpu",
            )["model_state_dict"]
        )
        self.model.eval()
        self.classes_key = classes_key

    def detect(self, img):
        with torch.no_grad():
            result = self.model(img)
            result = nn.softmax(dim=1)(result)
            return pd.DataFrame(np.column_stack([list(self.classes_key.keys()), list(self.classes_key.values()), result.numpy()[0]]), columns=['classid','classname','confidence'])