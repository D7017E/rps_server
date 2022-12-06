import numpy as np
import cv2
import base64
import re
import os
from util.serialize_image import deserialize_image
from flask import Flask, request, send_file

import ai_mediapipe
from prediction import Prediction

app = Flask(__name__)
ai_mediapipe.load_model("gesture_train.csv")

def weighted_prediction(prediction_list: list) -> Prediction:
    """Takes the list of individual predictions and returns the weighted 
    output. Later predictions are valued higher."""
    predictions: dict = Prediction.empty_prediction_dict()
    for i, prediction in enumerate(prediction_list):
        try:
            predictions[prediction] += 1 + (i / (len(prediction_list) * 2))
        except:
            print("Unhandled prediction")
    prediction = max(predictions, key=predictions.get)
    return prediction


def predict_image(image: np.ndarray) -> Prediction:
    """Redirects a single image to mediapipe for prediction and returns the 
    result."""
    prediction: Prediction = ai_mediapipe.predict(image, True)
    return prediction


def predict_list(req_body: str) -> Prediction:
    """Take in the list of serialized images in the form of a JSON, decodes 
    them and send them to predict_image to get a prediction for each individual 
    image. Returns a weighted prediction in the form of a string."""
    image_list = req_body["image_list"]
    shape = tuple(req_body["shape"])

    predictions = []
    for image in image_list:
        image_bytes = base64.b64decode(image.encode("utf8"))
        deserialized_image = deserialize_image(image_bytes, np.uint8, shape)
        predictions.append(predict_image(deserialized_image))

    prediction = weighted_prediction(predictions)
    return prediction

@app.route("/predict/hand", methods=['GET'])
def predict_hand():
    req_body = request.get_json()
    prediction: Prediction = predict_list(req_body)
    return {"prediction": prediction.name}, 200

@app.route("/predict/hand/image/<filename>", methods=['GET'])
def predict_hand_image(filename):
    # Remove surrounding whitespace and check if the filename only contains 
    # alphanumeric characters, dots and underscores.
    filename = filename.strip()
    if not re.match(r"^[\w\d._]*$", filename):
        return "Invalid filename", 400
    
    filepath = os.path.join(os.path.dirname(__file__), '../saved_models/data_collection/', filename)
    if not os.path.isfile(filepath):
        return "File not found", 404

    return send_file(filepath), 200
