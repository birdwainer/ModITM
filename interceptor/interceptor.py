"""
This file is a bottle webserver that intercepts and modifies images as they are 
transmitted across a network using a computer vision model. 
"""
from bottle import route, response, run
from ruamel.yaml import YAML
import pandas as pd

import cv2
import torch
import httpx
import numpy as np
from typing import Dict
import numpy.typing as npt

from model import ResNet18

evil_model = ResNet18()


def has_class_over_threshold(df: pd.DataFrame, cfg: Dict[str, Dict[str, float]]) -> bool:
    """Determine if a data frame has any class with an overlap of at least `target_classes`
    in the `class_names` list and if it is over the confidence specified in the configuration
    file.

    Args:
        df (pd.DataFrame): The data frame to check.

    Returns:
        bool: Whether any class in `df` has an overlap of at least `target_classes` with `class_names`
        that are over the confidence threshold for the class.
    """
    hcot = False
    intersected = set(df["name"].tolist()).intersection(class_names)

    if len(intersected) > 0:
        for _, row in df[df["name"].isin(intersected)].iterrows():
            if row["confidence"] >= cfg["target_classes"][row["name"]]:
                hcot = True
                break

    return hcot


def invert_img(image: npt.NDArray[np.float32]) -> bytes:
    """Inverts an image by taking its bitwise NOT.

    Args:
        image (np.NDArray[npt.float32]): The input image to be inverted.

    Returns:
        bytes: The inverted image as a byte array.
    """
    image = cv2.bitwise_not(image)
    neg_bytes = cv2.imencode(".jpg", image)[1].tostring()
    return neg_bytes


def obliterate_img(image: npt.NDArray[np.float32]) -> bytes:
    """Obliterates an image by setting all pixels to zero.

    Args:
        image (np.NDArray[npt.float32]): The image to be obliterated.

    Returns:
        bytes: The obliterated image as a JPEG-encoded byte string.
    """
    image = np.zeros((32, 32, 3), np.uint8)
    return cv2.imencode(".jpg", image)[1].tostring()


def replace_img() -> bytes:
    """Replaces all images with a click.png image in the HTML content.

    Returns:
        bytes: Returns a bytestring for the replacement image.
    """
    with open("images/click.png", "rb") as img_file:
        image_bytes = img_file.read()
    return image_bytes


def read_config() -> Dict[str, Dict[str, float]]:
    """Reads the configuration file and returns a dictionary containing its contents.

    Returns:
        Dict[str, float]: A dictionary containing the class and confidence
    """
    with open("/config/config.yaml", "r") as cfg_file:
        yaml = YAML(typ="safe")
        cfg = yaml.load(cfg_file)
    return cfg


@route("/image/<position:int>")
def moditm(position: int) -> bytes:
    """Run model on intercepted images and, if it is a class of interest, replace
    the image with another.

    Args:
        position (int): The image to pull from format <IP>/image/<integer>

    Returns:
        bytes: return a jpeg image bytestring.
    """
    server_ip = "192.168.1.222"
    forwarding_uri = f"http://{server_ip}/image/{position}"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    image = np.asarray(bytearray(img_bytes), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = torch.from_numpy(image.transpose(2, 1, 0)).unsqueeze(0).type(torch.float32)
    result = evil_model.detect(image)

    if not result.empty and has_class_over_threshold(result, cfg):
        img_bytes = replace_img()
    response.set_header("Content-type", "image/jpeg")
    return img_bytes


cfg = read_config()
class_names = set(cfg["target_classes"].keys())

run(host="0.0.0.0", port=5000, debug=True)
