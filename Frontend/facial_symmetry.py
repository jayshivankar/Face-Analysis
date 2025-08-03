import cv2
import mediapipe as mp
import numpy as np


# Initialize mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Landmark indices for symmetry (sample key regions)
LEFT_POINTS = [33, 159, 145, 61, 78, 95]        # left eye, cheek, mouth corner
RIGHT_POINTS = [263, 386, 374, 291, 308, 324]   # mirrored right side
MIDLINE_POINTS = [1, 168, 199]                  # nose bridge, chin

# Thresholds to determine symmetry(lower the number,more symmetric it is)
ASYMMETRY_THRESHOLDS = 0.04

# Analyze facial asymmetry and predict possible conditions.
def analyze_symmetry(image:np.ndarray) -> dict:
    results = face_mesh.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return {"error": "No face detected"}

    landmarks = results.multi_face_landmarks[0].landmark
    h,w = image.shape[:2]