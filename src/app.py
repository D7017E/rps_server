import os
import numpy as np
import base64
# import ai_tensorflow
import ai_mediapipe
from dotenv import load_dotenv
from flask import Flask, flash, request, redirect, url_for
from util.serialize_image import serialize_image, serialize_image_array, deserialize_image

load_dotenv()

app = Flask(__name__)

# Load AI model
# ai_model_name = os.environ.get("AI_MODEL_NAME", "pneumonia")
# ai_model_input_shape = os.environ.get("AI_INPUT_SHAPE", "(1, 100, 100, 1)")
# ai.load_model(ai_model_name, ai_model_input_shape)
# print(f"AI model: successfully loaded model '{ai_model_name}'")
ai_mediapipe.load_model("gesture_train.csv")


def predictImage(image):
    prediction = ai_mediapipe.predict(image)
    return prediction

def weightedPrediction(imageList):
    print("dummy")

"""
    req[
        body[
            imageList[
                image: ----
            ]
            shape: ----
        ]
    ]
"""

def predict_list(req_body):
    image_list = req_body["image_list"]
    shape = req_body["shape"]
    predictions = []
    for i in req_body:
        image_bytes = base64.b64decode(image_list["image"].encode("utf8"))
        image = deserialize_image(image_bytes, np.uint8, shape)
        predictions.append(predictImage(image))

    return prediction

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/hand", methods=['GET'])
def predict_hand():
    req_body = request.get_json()
    shape = req_body["shape"]

    prediction = predict_list(req_body)
    # try:
    #     prediction = ai.predict(image)
    # except ai.AIException as e:
    #     return {"error": str(e)}, 400
    # except:
    #     return {"error": "Internal server error"}, 500

    return {"prediction": prediction}, 200

