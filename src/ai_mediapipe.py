import os
import cv2
import mediapipe as mp
import numpy as np
from prediction import Prediction
from imagebox import ImageBox
import uuid

ai_model_dir = os.path.join(os.path.dirname(__file__), "../saved_models/")

hands = None
knn = None

def load_model(joint_document):
    joint_path = os.path.join(ai_model_dir, joint_document)
    if not os.path.exists(joint_path):
        raise Exception(f"{joint_path}: No such file or directory")

    max_num_hands = 1

    # MediaPipe hands model
    mp_hands = mp.solutions.hands
    global hands
    hands = mp_hands.Hands(
        max_num_hands=max_num_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    # Gesture recognition model
    file = np.genfromtxt(joint_path, delimiter=',')
    angle = file[:,:-1].astype(np.float32)
    label = file[:, -1].astype(np.float32)
    global knn
    knn = cv2.ml.KNearest_create()
    knn.train(angle, cv2.ml.ROW_SAMPLE, label)


def predict(image, generate_data=False) -> (Prediction, ImageBox or None):
    """
    Predict the gesture from the image.

    Parameters
    ----------
    image : np.array
        The image to predict the gesture from
    generate_data : bool, optional
        If true, the data will be saved to csv and jpg files, by default False
    
    Returns
    -------
    Tuple(Prediction, ImageBox or None)
        The predicted gesture and the image box containing the saved images, 
        image box will be `None` if generate_data is `False`.
    """
    image_raw = image.copy()
    result = hands.process(image)

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Compute angles between joints
            v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
            v = v2 - v1 # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum('nt,nt->n',
                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

            angle = np.degrees(angle) # Convert radian to degree

            # Inference gesture
            data = np.array([angle], dtype=np.float32)
            ret, results, neighbours, dist = knn.findNearest(data, 3)
            idx = int(results[0][0])
            
            images = None
            if generate_data:
                # Place captured gesture on image
                cv2.putText(image, text=Prediction(idx).name, org=(int(res.landmark[0].x * image.shape[1]), int(res.landmark[0].y * image.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
                mp.solutions.drawing_utils.draw_landmarks(image, res, mp.solutions.hands.HAND_CONNECTIONS)
                # Save data
                images = save_data_to(data, image_raw, image)
            return Prediction(idx), images
    else:
        return Prediction(0), None

def save_data_to(data, image_raw, image_processed) -> ImageBox:
    """
    Save joint data to csv file and images to jpg files. The filenames will be 
    a unique id for the joint data and the images.

    The files generated are:
    - <id>.csv: The joint data
    - <id>_raw.jpg: The raw image
    - <id>_processed.jpg: The processed image

    Parameters
    ----------
    data : np.array
        The joint data
    image_raw : np.array
        The raw image without any gestures
    image_processed : np.array
        The processed image with the gesture
    
    Returns
    -------
    ImageBox
        The image box containing the saved images.
    """
    data_id = uuid.uuid4().hex
    joint_filename = data_id + ".csv"
    image_raw_filename = data_id + "_raw.jpg"
    image_processed_filename = data_id + "_processed.jpg"

    path_to_directory = os.path.join(ai_model_dir, "data_collection")
    if not os.path.exists(path_to_directory):
        os.makedirs(path_to_directory)

    joint_filepath = os.path.join(path_to_directory, joint_filename)
    image_raw_filepath = os.path.join(path_to_directory, image_raw_filename)
    image_processed_filepath = os.path.join(path_to_directory, image_processed_filename)

    joint_coordinates_str = ",".join(map(str, np.around(data[0], decimals=6)))

    f = open(joint_filepath, "w")
    f.write(joint_coordinates_str)
    f.close()
    cv2.imwrite(image_raw_filepath, image_raw)
    cv2.imwrite(image_processed_filepath, image_processed)

    return ImageBox(image_raw_filename, image_processed_filename)
