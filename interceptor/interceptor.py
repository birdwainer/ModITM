from bottle import route, response, run

import cv2
import httpx
import numpy as np


from model import YOLOv5

TARGET_CLASSES = [
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
]
evil_model = YOLOv5()


@route("/image")
def moditm():
    server_ip = "192.168.1.222"
    path = "/image"
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


run(host="0.0.0.0", port=5000, debug=True)
