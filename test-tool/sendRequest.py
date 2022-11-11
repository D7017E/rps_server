import sys
sys.path.append("../src")
sys.path.append("./src")

import base64
import json
import requests
import numpy as np
from util.serialize_image import serialize_image, serialize_image_array, deserialize_image

def make_request(image):
    """
    Send a request to the server.

    Parameters
    ----------
    image : numpy.ndarray
        The image to send to the server
    """
    image_bytes = serialize_image_array(image)
    image_str = base64.b64encode(image_bytes).decode("utf8")

    request_body = json.dumps({
        "image": image_str,
        "dtype": image.dtype.name,
        "shape": list(image.shape)
    })
    print(request_body)
    request_headers = headers={"Content-Type": "application/json"}

    URL = "http://127.0.0.1:5000/predict/hand"
    response = requests.get(URL, data=request_body, headers=request_headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Something went wrong, status code: {response.status_code}")


if __name__ == "__main__":
    image = np.array([[[36,28,237],[76,177,34]],[[232,162,0],[255,255,255]]], dtype=np.uint8)
    make_request(image)
