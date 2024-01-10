import numpy as np
import pandas as pd
import torch
import random


class FakeModel:
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

    FAKE_TENSOR_LS = [
        torch.Tensor([[0.7, 0.2, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),
        torch.Tensor([[0.3, 0.5, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.1]]),
        torch.Tensor([[0.0, 0.6, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3]]),
    ]

    def __init__(self, fake_tensors=FAKE_TENSOR_LS, classes_key=CLASSES_KEY):
        self.fake_tensors = fake_tensors
        self.classes_key = classes_key

    def detect(self, *args, **kwargs):
        result = random.choice(self.fake_tensors)

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


if __name__ == "__main__":
    img = torch.randn((1, 3, 32, 32))
    model = FakeModel()
    result = model.detect(img)
    print(result.shape)
