import os
import cv2
import mediapipe as mp
import numpy as np
from prediction import Prediction

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Mediapipe(metaclass=Singleton):
    __ai_model_dir = os.path.join(os.path.dirname(__file__), "../saved_models/")
    __hands = None
    __knn = None

    def __init__(self, csv) -> None:
        self.load_model(csv, self.__ai_model_dir)
        

    def __load_model(self, joint_document, model_dir):
        joint_path = os.path.join(model_dir, joint_document)
        if not os.path.exists(joint_path):
            raise AIException(f"{joint_path}: No such file or directory")

        max_num_hands = 1

        # MediaPipe hands model
        mp_hands = mp.solutions.hands
        self.__hands = mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        # Gesture recognition model
        file = np.genfromtxt(joint_path, delimiter=',')
        angle = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        self.__knn = cv2.ml.KNearest_create()
        self.__knn.train(angle, cv2.ml.ROW_SAMPLE, label)


    def __predict(self, image) -> Prediction:
        img = cv2.flip(image, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = self.__hands.process(img)

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
                ret, results, neighbours, dist = self.__knn.findNearest(data, 3)
                idx = int(results[0][0])

                return Prediction(idx)
        else:
            return Prediction(0)

class AIException(Exception):
    """Exception class for AI errors."""
    pass
