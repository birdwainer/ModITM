from bottle import route, request, response, run
from PIL import Image

import cv2 
import httpx
import io
import numpy as np 
import pandas as pd


from model import Yolov5

TARGET_CLASSES = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
evil_model = Yolov5()

@route('/image')
def moditm():
    server_ip = "192.168.1.222"
    path = "/image"
    forwarding_uri = f"http://{server_ip}{path}?"
    resp = httpx.get(forwarding_uri)
    img_bytes = resp.content

    # read image as an numpy array 
    image = np.asarray(bytearray(img_bytes), dtype="uint8") 
      
    # use imdecode function 
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) 

    result = evil_model.detect(image)
    df = pd.DataFrame(result)
    if df.iloc[0]['name'] in TARGET_CLASSES:
        img_bytes = invert_img(img_bytes)
    response.set_header('Content-type', 'image/jpeg')
    return img_bytes

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


