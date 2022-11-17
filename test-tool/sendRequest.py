import sys
sys.path.append("../src")
sys.path.append("./src")

import ai_mediapipe
import cv2
import base64
import json
import numpy as np
import requests
from util.serialize_image import serialize_image

def make_http_request_to_ai(images, grayscale):
    """
    Send a request to the server.

    Parameters
    ----------
    image : numpy.ndarray
        The image to send to the server
    grayscale : bool
        Whether the image is grayscale or not
    """
    print("Preparing request...")
    serialized_images = []
    for image in images:
        image_bytes, shape, channel_type = serialize_image(image, grayscale)
        image_str = base64.b64encode(image_bytes).decode("utf8")
        serialized_images.append(image_str)

    request_body = json.dumps({
        "image_list": serialized_images,
        "dtype": channel_type.name,
        "shape": list(shape)
    })
    
    request_headers = {"Content-Type": "application/json"}

    URL = "http://127.0.0.1:5000/predict/hand"
    print("Sending request...")
    response = requests.get(URL, data=request_body, headers=request_headers)
    print("Response received\n")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Something went wrong.")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")


def make_local_prediction(path):
    image = cv2.imread(path)
    ai_mediapipe.load_model()
    pred = ai_mediapipe.predict(image)
    print(pred)

if __name__ == "__main__":
    make_http_request_to_ai(["./images/elie_rock.jpg"], False)

