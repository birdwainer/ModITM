import torch


class YOLOv5:
    WEIGHTS_PATH = "./weights/yolov5n.pt"

    def __init__(self, weights_path=WEIGHTS_PATH):
        self.weights_path = weights_path  # relative path to weights
        self.model = torch.hub.load(
            "ultralytics/yolov5:v6.2",
            "custom",
            path=self.weights_path,
            device="cuda:0" if torch.cuda.is_available() else "cpu",
            _verbose=False,
            trust_repo=True,
        )

    def detect(self, img):
        results = self.model(img)
        return results.pandas().xyxy[
            0
        ]  # xmin ymin xmax ymax confidence class# classname
