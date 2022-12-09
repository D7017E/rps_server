import numpy as np
import cv2
import base64
import re
import os
from util.serialize_image import deserialize_image
from flask import Flask, request, send_file
from imagebox import ImageBox

import ai_mediapipe
from prediction import Prediction

RPS_SCHEMA_HOSTNAME = os.environ.get("RPS_SCHEMA_HOSTNAME", "http://localhost:5000/")

app = Flask(__name__)
ai_mediapipe.load_model("gesture_train.csv")

def weighted_prediction(prediction_list: list[tuple[Prediction, ImageBox or None]]) -> tuple[Prediction, ImageBox or None]:
    """
    Takes the list of individual predictions and returns the weighted 
    output. Later predictions are valued higher.

    Parameters
    ----------
    prediction_list : list[tuple[Prediction, ImageBox or None]]
        The list of individual predictions
    """
    predictions: dict[int, int] = Prediction.empty_prediction_dict()
    for i, prediction in enumerate(prediction_list):
        try:
            predictions[prediction[0]] += 1 + (i / (len(prediction_list) * 2))
        except:
            print("Unhandled prediction")
    prediction = max(predictions, key=predictions.get)
    print(prediction)

    # Get the data id for the prediction
    filtered_prediction_list = list(filter(lambda pred: pred[0] == prediction, prediction_list))
    prediction_data_id = filtered_prediction_list[0][1] if len(filtered_prediction_list) > 0 else None
    return (prediction, prediction_data_id)


def predict_image(image: np.ndarray) -> tuple[Prediction, ImageBox or None]:
    """
    Redirects a single image to mediapipe for prediction and returns the 
    result.

    Parameters
    ----------
    image : np.ndarray
        The image to predict the gesture from
    
    Returns
    -------
    Tuple(Prediction, ImageBox or None)
        The predicted gesture and the image box containing the saved images, 
        image box will be `None` if generate_data is `False`.
    """
    return ai_mediapipe.predict(image, True)


def predict_list(req_body: dict) -> tuple[Prediction, ImageBox or None]:
    """
    Take in the list of serialized images in the form of a JSON, decodes 
    them and send them to predict_image to get a prediction for each individual 
    image. Returns a weighted prediction in the form of a string.

    Parameters
    ----------
    req_body : dict
        The request body containing the list of images and the information
        about the images
    
    Returns
    -------
    Tuple(Prediction, ImageBox or None)
        The predicted gesture and the image box containing the saved images, 
        image box will be `None` if generate_data is `False`.
    """
    image_list = req_body["image_list"]
    shape = tuple(req_body["shape"])

    predictions: list[tuple[Prediction, ImageBox or None]] = []
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
    res_body = {
        "prediction": prediction[0].name, 
        "images": prediction[1].get_absolute_paths(os.path.join(RPS_SCHEMA_HOSTNAME,"predict/hand/image/")) if prediction[1] is not None else None
    }
    return res_body, 200

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
