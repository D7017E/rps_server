import sys
sys.path.append("../src")
sys.path.append("./src")

import base64
import json
import numpy as np
import requests
from util.serialize_image import serialize_image

def make_request_to_pneumonia_model(image, grayscale):
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
    image_bytes = serialize_image(image, grayscale)
    image_str = base64.b64encode(image_bytes).decode("utf8")

    request_body = json.dumps({
        "image": image_str,
        "dtype": np.uint8.__name__,
        "shape": [1, 100, 100, 1]
    })
    
    request_headers = headers={"Content-Type": "application/json"}

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


if __name__ == "__main__":
    make_request_to_pneumonia_model("./images/scaled_pneumonia.jpeg", True)
