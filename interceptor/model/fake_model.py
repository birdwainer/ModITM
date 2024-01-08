import torch
import random


class FakeModel:
    FAKE_TENSOR_LS = [
        torch.Tensor([[0.7, 0.2, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),
        torch.Tensor([[0.3, 0.5, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.1]]),
        torch.Tensor([[0.0, 0.6, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.1, 0.3]]),
    ]

    def __init__(self, fake_tensors=FAKE_TENSOR_LS):
        self.fake_tensors = fake_tensors

    def detect(self, *args, **kwargs):
        return random.choice(self.fake_tensors)


if __name__ == "__main__":
    img = torch.randn((1,3,32,32))
    model = FakeModel()
    result = model.detect(img)
    print(result.shape)