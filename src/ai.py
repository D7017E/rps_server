import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"

import tensorflow as tf
import numpy as np
from ast import literal_eval

ai_model_dir = os.path.join(os.path.dirname(__file__), "../saved_models/")
model = None
model_input_shape = None

def load_model(model_name, input_shape):
    """
    Load the AI model from the saved_models directory in project root. Input 
    shape is a tuple of the input shape required by the loaded model.

    Parameters
    ----------
    model_name : str
        Name of the model to load. The model must be in the `saved_models` 
        directory in the project root.

    input_shape : tuple
        Shape of the input to the model. This is used to reshape the input 
        image to the correct shape. The shape must be a tuple of integers.
    
    Returns
    -------
    None

    Examples
    --------
    Load a model named `my_model` with input shape `(128, 128, 3)` e.g. an 
    array of 128x128 RGB images:
    >>> load_model("my_model", (128, 128, 3))
    """
    global model_input_shape, model

    # Eval input shape
    try:
        model_input_shape = literal_eval(input_shape)
    except:
        raise AIException("Invalid input shape when loading model")

    # Load model
    model_path = os.path.join(ai_model_dir, model_name)
    if not os.path.exists(model_path):
        raise AIException(f"{model_path}: No such file or directory")
    model = tf.keras.models.load_model(model_path)

def predict(image):
    """
    Predict the output of the loaded model given an input image as a numpy array.

    Parameters
    ----------
    image : numpy.ndarray
        Input image to feed the model. The shape of the image must match the 
        input specified when loading the model.

    Returns
    -------
    int
        The predicted output of the model.
    """

    # Check model is loaded
    if model is None:
        raise AIException("Model not loaded")

    if image is None:
        raise AIException("Image must not non-empty")

    # Check input shape
    if image.shape != model_input_shape:
        raise AIException("Shape of input image does not match required model input shape")
    
    return int(np.argmax(model.predict(image)[0]))

class AIException(Exception):
    """Exception class for AI errors."""
    pass
