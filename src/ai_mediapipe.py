import os
import cv2
import mediapipe as mp
import numpy as np
from prediction import Prediction
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


def predict(image, generate_data=False) -> Prediction:
    img = cv2.flip(image, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img)

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
            if save_data:
                save_data_to(data, image)
            return Prediction(idx)
    else:
        return Prediction(0)

def save_data_to(data, image):
    data_id = uuid.uuid4().hex
    joint_filename = data_id + ".csv"
    image_filename = data_id + ".jpg"

    path_to_directory = os.path.join(ai_model_dir, "data_collection")
    if not os.path.exists(path_to_directory):
        os.makedirs(path_to_directory)

    joint_filepath = os.path.join(path_to_directory, joint_filename)
    image_filepath = os.path.join(path_to_directory, image_filename)

    joint_coordinates_str = ",".join(map(str, np.around(data[0], decimals=6)))

    f = open(joint_filepath, "w")
    f.write(joint_coordinates_str)
    f.close()
    cv2.imwrite(image_filepath, image)

    print("Saved data to: " + joint_filepath)
