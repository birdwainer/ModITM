import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18


class ResNet18:
    WEIGHTS_PATH = "../weights/best.pt"

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
            nn.Softmax(dim=1),
        )
        self.model.load_state_dict(
            torch.load(
                weights_path,
                map_location="cuda:0" if torch.cuda.is_available() else "cpu",
            )["model_state_dict"]
        )
        self.model.eval()
        self.classes_key = classes_key
        self.transformations = transforms.Compose(
            [
                transforms.Normalize(
                    [0.49118733, 0.48202792, 0.44637883],
                    [0.24694054, 0.24337897, 0.26151666],
                ),
            ]
        )

    def detect(self, img):
        with torch.no_grad():
            img = self.transformations(img)
            result = self.model(img)
            return result
            # return self.classes_key[result.argmax(1).item()]


if __name__ == "__main__":
    import cv2
    from PIL import Image
    import numpy as np

    IMG_PATH = "/Users/achadda/Desktop/ModITM_rev2/images/CFAIR-10/automobile/66.png"
    model = ResNet18(
        weights_path="/Users/achadda/Desktop/ModITM_rev2/interceptor/weights/best.pt"
    )

    image = np.array(Image.open(IMG_PATH), dtype="uint8")
    image = torch.from_numpy(image.transpose(2, 1, 0)).unsqueeze(0).type(torch.float32)
    result = model.detect(image)

    # print(torch.exp(result))
    print(result.shape)
    print(result)
