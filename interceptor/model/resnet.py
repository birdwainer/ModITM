import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torchvision.models import resnet18


class ResNet18:
    WEIGHTS_PATH = "/config/weights/best.pt"

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
        self.model = resnet18(weights=None, num_classes=10)
        self.model.conv1 = nn.Conv2d(
            3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False
        )
        self.model.maxpool = nn.Identity()
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
            result = nn.functional.softmax(result, dim=1)
            ret = pd.DataFrame(
                np.column_stack(
                    [
                        list(self.classes_key.keys()),
                        list(self.classes_key.values()),
                        result.numpy()[0],
                    ]
                ),
                columns=["id", "name", "confidence"],
            )
            ret["id"] = pd.to_numeric(ret["id"])
            ret["confidence"] = pd.to_numeric(ret["confidence"])
            return ret
