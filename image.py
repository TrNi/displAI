import openai
from PIL import Image
import cv2
import base64
import io
import numpy

# Take in base64 string and return cv image
def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata))
    opencv_img= cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)
    return opencv_img

PROMPT = "An eco-friendly computer from the 90s in the style of vaporwave"

#openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="1024x1024",
    response_format="b64_json",
)


for index, image_dict in enumerate(response["data"]):
    image_data = stringToRGB(image_dict["b64_json"])
    cv2.imshow('test', image_data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
