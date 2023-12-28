import glob
import random
from bottle import route, response, run, static_file


def select_random_image(root, glob_target):
    files = glob.glob(root + glob_target)
    print(files)
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


@route("/image_one")
@route("/image_two")
def send_captcha_image_ship():
    response.set_header("Content-type", "image/jpeg")
    return select_random_image("/images/CFAIR-10/ship/", "*.png")


@route("/image_three")
@route("/image_four")
@route("/image_five")
@route("/image_six")
def send_captcha_image_car():
    response.set_header("Content-type", "image/jpeg")
    return select_random_image("/images/CFAIR-10/automobile/", "*.png")


@route("/image_seven")
@route("/image_eight")
@route("/image_nine")
def send_captcha_image_plane():
    response.set_header("Content-type", "image/jpeg")
    return select_random_image("/images/CFAIR-10/airplane/", "*.png")


run(host="0.0.0.0", port=80, debug=True)
