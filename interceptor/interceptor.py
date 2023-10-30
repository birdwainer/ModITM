from bottle import route, request, response, run
from PIL import Image

import httpx
import io


@route('/axis-cgi/jpg/image.cgi')
def moditm():
    #Sample URI
    #http://192.168.1.222/axis-cgi/jpg/image.cgi?resolution=1920x1080&compression=5&camera=1
    camera_ip = "192.168.1.222"
    path = "/axis-cgi/jpg/image.cgi"
    resolution = request.query.resolution
    compression = request.query.compression
    camera_id = request.query.camera
    forwarding_uri = f"http://{camera_ip}{path}?resolution={resolution}&compression={compression}&camera={camera_id}"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content
    inverted = invert_img(img_bytes)
    response.set_header('Content-type', 'image/jpeg')
    return inverted

def invert_img(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    negative = img
    width,height = img.size
    for i in range(width):
        for j in range(height):
            r,g,b=img.getpixel((i,j))
            nr=255-r
            ng=255-g
            nb=255-b
            negative.putpixel((i,j),(nr,ng,nb))

    neg_bytes = io.BytesIO()
    negative.save(neg_bytes, format=img.format)
    return neg_bytes.getvalue()

run(host='0.0.0.0', port=5000, debug=True)


