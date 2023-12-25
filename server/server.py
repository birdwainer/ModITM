import glob
import os
import random
from bottle import route, request, response, run, static_file


@route("/image")
def random_image():
    base_uri = "/images/VOCdevkit/VOC2012/JPEGImages/"
    ext = "*.jpg"
    files = glob.glob(base_uri + ext)

    selected = random.choice(files)
    img_bytes = None
    with open(selected, "rb") as img_file:
        img_bytes = img_file.read()

    response.set_header("Content-type", "image/jpeg")
    return img_bytes


@route("/<filename:re:.*\.js>")
def send_js(filename):
    return static_file(filename, root="./js/")


@route("/<filename:re:.*\.css>")
def send_css(filename):
    return static_file(filename, root="./css/")


@route("/")
def index():
    return open("./html/index.html").read()

@route("/<filename:re:.*\.(ico)>")
def send_favicon(filename):
    return static_file(filename, root="./images/")
# @route("/<filename:re:.*\.(jpg|png|ico)>")

run(host="0.0.0.0", port=80, debug=True)
