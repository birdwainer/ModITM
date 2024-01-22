"""
This file serves as a web server that displays images from the CIFAR-10 dataset. 
The images are randomly selected and displayed on the index page. The user can 
click on an image to receive a random number between 1 and 9, which is used to 
select a new image. The favicon.ico and Image Logo are also served by this file.
"""
import glob
import os
import random
from json import dumps
from bottle import HTTPError, route, response, run, static_file


def select_random_image(root: str, glob_target: str) -> bytes:
    """Select a random image from the given directory using a glob pattern.

    Args:
        root (str): The path to the directory containing the images.
        glob_target (str): The glob pattern used to search for images in the directory.

    Returns:
        bytes: The binary data of the selected image.
    """
    files = glob.glob(root + glob_target)
    candidate = random.choice(files)
    image_bytes = None
    with open(candidate, "rb") as img_file:
        image_bytes = img_file.read()
    return image_bytes


@route("/<filename:re:.*\.js>")
def send_js(filename: str) -> bytes:
    """Send JavaScript file.

    Args:
        filename (str): Relative path of the JavaScript file to send.

    Returns:
        Response: Bottle response object containing the JavaScript file.
    """
    return static_file(filename, root="./js/")


@route("/<filename:re:.*\.css>")
def send_css(filename: str) -> bytes:
    """Send CSS file.

    Args:
        filename (str): Relative path of the CSS file to send.

    Returns:
        _type_: _description_
    """
    return static_file(filename, root="./css/")


@route("/")
def index() -> str:
    """Send HTML file.

    Returns:
        str: Contents of HTML file as a string.
    """
    return open("./html/index.html").read()


@route("/<filename:re:.*\.(ico)>")
def send_favicon(filename: str) -> bytes:
    """Send favicon.ico file.

    Args:
        filename (str): Relative path of the .ico file to send.

    Returns:
        _type_: _description_
    """
    return static_file(filename, root="./images/")


@route("/<filename:re:.*\.(png)>")
def send_labs_logo(filename: str) -> bytes:
    """Send Image Logo file.

    Args:
        filename (str): Relative path of the .png file to send.

    Returns:
        _type_: _description_
    """
    return static_file(filename, root="./images/")


@route("/image/<position:int>")
def send_captcha_image(position: int) -> bytes:
    """Sends a random captcha image for the given position.

    Args:
        position (int): The position of the captcha to send.

    Returns:
        bytes: The binary data of the selected image file.

    Raises:
        HTTPError: If the requested position is not found or an invalid value.
    """
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

    loc = os.path.join("/images/CIFAR-10/", vehicle_type)
    response.set_header("Content-type", "image/jpeg")

    return select_random_image(loc, "*.png")


run(host="0.0.0.0", port=80, debug=True)
