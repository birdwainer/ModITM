from bottle import route, response, run

import cv2
import torch
import httpx
import numpy as np

from model import ResNet18

TARGET_CLASSES = [
    "car",
]

evil_model = ResNet18()


def moditm(path):
    server_ip = "192.168.1.222"
    forwarding_uri = f"http://{server_ip}{path}?"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    image = np.asarray(bytearray(img_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = torch.from_numpy(image.transpose(2, 1, 0)).unsqueeze(0).type(torch.float32)
    result = evil_model.detect(image)

    if result in TARGET_CLASSES:
        img_bytes = obliterate_img(image)
    response.set_header("Content-type", "image/jpeg")
    return img_bytes


def obliterate_img(image):
    image = np.zeros((32, 32, 3), np.uint8)
    return cv2.imencode(".jpg", image)[1].tostring()


@route("/image_one")
def execute_moditm():
    path = "/image_one"
    return moditm(path)


@route("/image_two")
def execute_moditm():
    path = "/image_two"
    return moditm(path)


@route("/image_three")
def execute_moditm():
    path = "/image_three"
    return moditm(path)


@route("/image_four")
def execute_moditm():
    path = "/image_four"
    return moditm(path)


@route("/image_five")
def execute_moditm():
    path = "/image_five"
    return moditm(path)


@route("/image_six")
def execute_moditm():
    path = "/image_six"
    return moditm(path)


@route("/image_seven")
def execute_moditm():
    path = "/image_seven"
    return moditm(path)


@route("/image_eight")
def execute_moditm():
    path = "/image_eight"
    return moditm(path)


@route("/image_nine")
def execute_moditm():
    path = "/image_nine"
    return moditm(path)


run(host="0.0.0.0", port=5000, debug=True)
