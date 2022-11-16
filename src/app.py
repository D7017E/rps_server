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
ai_mediapipe.load_model()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict/hand", methods=['GET'])
def predict_hand():
    req_body = request.get_json()

    image_bytes = base64.b64decode(req_body["image"].encode("utf8"))
    image_shape = tuple(req_body["shape"])
    image = deserialize_image(image_bytes, np.uint8, image_shape)

    prediction = ai_mediapipe.predict(image)
    # try:
    #     prediction = ai.predict(image)
    # except ai.AIException as e:
    #     return {"error": str(e)}, 400
    # except:
    #     return {"error": "Internal server error"}, 500

    return {"prediction": prediction}, 200

