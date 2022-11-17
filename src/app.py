import os
import numpy as np
import base64
# import ai_tensorflow
import ai_mediapipe
from prediction import Prediction
from flask import Flask, flash, request, redirect, url_for
from util.serialize_image import serialize_image, serialize_image_array, deserialize_image

# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

# Load AI model
# ai_model_name = os.environ.get("AI_MODEL_NAME", "pneumonia")
# ai_model_input_shape = os.environ.get("AI_INPUT_SHAPE", "(1, 100, 100, 1)")
# ai.load_model(ai_model_name, ai_model_input_shape)
# print(f"AI model: successfully loaded model '{ai_model_name}'")
ai_mediapipe.load_model("gesture_train.csv")


# Takes the list of individual predictions and returns the weighted output. later predictions are valued higher.
<<<<<<< HEAD
def weighted_prediction(prediction_list: list) -> Prediction:
    predictions: dict = Prediction.empty_prediction_dict()
    for prediction in prediction_list:
=======
def weighted_prediction(prediction_list: list) -> str:
    predictions = {
        "fail": 0,
        "nothing": 0,
        "rock": 0,
        "paper": 0,
        "scissors": 0,
    }
    for i, prediction in enumerate(prediction_list):
>>>>>>> fed7fff090901d87c9e318fc673d6ceadeda52ef
        try:
            predictions[prediction] += 1 + (i / (len(prediction_list) * 2))
        except:
            print("Unhandled prediction")
    prediction = max(predictions, key=predictions.get)
    return prediction


# Redirects a single image to mediapipe for prediction and returns the result.
def predict_image(image: np.ndarray) -> str:
    prediction = ai_mediapipe.predict(image)
    return prediction

"""
    mock up of the json structure
    req[
        body[
            imageList[
                image: ----
            ]
            shape: ----
        ]
    ]
"""

# Take in the list of serialized images in the form of a JSON, decodes them and send them to predict_image to get a prediction for each individual image.
# Returns a weighted prediction in the form of a string.
def predict_list(req_body: str) -> str:
    image_list = req_body["image_list"]
    shape = req_body["shape"]
    
    predictions = []
    for image in image_list:
        image_bytes = base64.b64decode(image.encode("utf8"))
        deserialized_image = deserialize_image(image_bytes, np.uint8, shape)
        predictions.append(predict_image(deserialized_image))

    prediction = weighted_prediction(predictions)
    return prediction

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/hand", methods=['GET'])
def predict_hand():
    req_body = request.get_json()

    prediction = predict_list(req_body)
    # try:
    #     prediction = ai.predict(image)
    # except ai.AIException as e:
    #     return {"error": str(e)}, 400
    # except:
    #     return {"error": "Internal server error"}, 500

    return {"prediction": prediction}, 200

