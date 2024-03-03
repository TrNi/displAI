import base64
import io
import numpy as np
import base64
from PIL import Image
import cv2

def strtoimg(b64str):
    imgdata = base64.b64decode((str(b64str)))
    img = Image.open(io.BytesIO(imgdata))
    return img
