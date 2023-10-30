import glob
import os
import random
from bottle import route, request, response, run

@route('/image')
def random_image():
    base_uri='/images/VOCdevkit/VOC2012/JPEGImages/'
    ext = '*.jpg'
    files = glob.glob(base_uri + ext)

    selected = random.choice(files)
    img_bytes = None
    with open(selected, 'rb') as img_file:
        img_bytes = img_file.read()

    response.set_header('Content-type', 'image/jpeg')
    return img_bytes

run(host='0.0.0.0', port=80, debug=True)


