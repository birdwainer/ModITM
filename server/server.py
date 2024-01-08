import glob
import os
import random
from bottle import HTTPError, route, response, run, static_file


def select_random_image(root, glob_target):
    files = glob.glob(root + glob_target)
    candidate = random.choice(files)
    image_bytes = None
    with open(candidate, "rb") as img_file:
        image_bytes = img_file.read()
    return image_bytes


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


@route("/<filename:re:.*\.(png)>")
def send_labs_logo(filename):
    return static_file(filename, root="./images/")


@route("/image/<position:int>")
def send_captcha_image_ship(position):
    vehicle_type = ""
    match position:
        case 1:
            vehicle_type = "ship/"
        case 2:
            vehicle_type = "ship/"
        case 3:
            vehicle_type = "automobile/"
        case 4:
            vehicle_type = "automobile/"
        case 5:
            vehicle_type = "automobile/"
        case 6:
            vehicle_type = "automobile/"
        case 7:
            vehicle_type = "airplane/"
        case 8:
            vehicle_type = "airplane/"
        case 9:
            vehicle_type = "airplane/"
        case _:
            return HTTPError(404, dumps("Not Found"), **response.headers)

    loc = os.path.join("/images/CFAIR-10/", vehicle_type)
    response.set_header("Content-type", "image/jpeg")
    
    return select_random_image(loc, "*.png")

run(host="0.0.0.0", port=80, debug=True)
