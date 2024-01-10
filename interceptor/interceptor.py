from bottle import route, response, run
from ruamel.yaml import YAML

import cv2
import torch
import httpx
import numpy as np

from model import ResNet18
from model import YOLOv5

evil_model = YOLOv5()


def has_class_over_threshold(df):
    hcot = False
    bboxes = list()
    intersected = set(df["name"].tolist()).intersection(class_names)

    if len(intersected) > 0:
        for idx, row in df[df["name"].isin(intersected)].iterrows():
            if row["confidence"] >= cfg["target_classes"][row["name"]]:
                hcot = True
                bboxes.append((row["xmin"],row["xmax"],row["ymin"],row["ymax"]))

    return hcot, bboxes


def invert_img(image):
    image = cv2.bitwise_not(image)
    neg_bytes = cv2.imencode(".jpg", image)[1].tobytes()
    return neg_bytes


def obliterate_img(image):
    image = np.zeros((32, 32, 3), np.uint8)
    return cv2.imencode(".jpg", image)[1].tobytes()


def replace_img_segment(image, bb_x_min, bb_x_max, bb_y_min, bb_y_max):
    dim = (bb_x_max - bb_x_min, bb_y_max - bb_y_min)
    replacement = cv2.resize(
        cv2.imread("images/dont_click.png"), dim
    )
    image[bb_y_min:bb_y_max, bb_x_min:bb_x_max] = replacement
    # for x in range(bb_x_min, bb_x_max):
    #     for y in range(bb_y_min, bb_y_max):
    #         image[x,y] = replacement.getpixel(x - bb_x_min, y - bb_y_min)
    return image


def read_config():
    with open("/config/config.yaml", "r") as cfg_file:
        yaml = YAML(typ="safe")
        cfg = yaml.load(cfg_file)
    return cfg


@route("/image")
def moditm():
    server_ip = "192.168.1.222"
    forwarding_uri = f"http://{server_ip}/image"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    image = np.asarray(bytearray(img_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # image = torch.from_numpy(image.transpose(2, 1, 0)).unsqueeze(0).type(torch.float32)
    result = evil_model.detect(image)
    hcot, bboxes = has_class_over_threshold(result)
    if not result.empty and len(bboxes) > 0:
        for bbox in bboxes:
            image = replace_img_segment(image, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
        img_bytes = cv2.imencode(".jpg", image)[1].tobytes()
    response.set_header("Content-type", "image/jpeg")
    return img_bytes


cfg = read_config()
class_names = set(cfg["target_classes"].keys())

run(host="0.0.0.0", port=5000, debug=True)
