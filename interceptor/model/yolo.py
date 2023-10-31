import torch

 

COCO_CLASSES_LS = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]

 

CLASSES = {idx: val for idx, val in enumerate(COCO_CLASSES_LS)}

 

class Yolov5():
    def __init__(self):
        self.weights_path = './best.pt' # relative path to weights
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.weights_path, device='cuda:0' if torch.cuda.is_available() else 'cpu',  _verbose=False)

 

    def detect(self, img):
        results = self.model(img)
        # print(f'{results.pandas().xyxy}')
        return results.pandas().xyxy[0] # xmin ymin xmax ymax confidence class# classname