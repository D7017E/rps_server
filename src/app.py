import os
import numpy as np
import base64
from flask import Flask, flash, request, redirect, url_for
from util.serialize_image import serialize_image, serialize_image_array, deserialize_image

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/hand", methods=['GET'])
def predict_hand():
    req_body = request.get_json()

    image_bytes = base64.b64decode(req_body["image"].encode("utf8"))
    image_shape = tuple(req_body["shape"])
    image = deserialize_image(image_bytes, np.uint8, image_shape).tolist()

    # TODO: Replace this with the AI model's prediction
    res = {
        "data": image
    }

    return res

