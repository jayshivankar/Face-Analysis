import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Landmark indices for symmetry (sample key regions)
LEFT_POINTS = [33, 159, 145, 61, 78, 95]    # e.g. left eye, cheek, mouth corner
RIGHT_POINTS = [263, 386, 374, 291, 308, 324]  # mirrored right side
MIDLINE_POINTS = [1, 168, 199]  # nose bridge, chin

# Thresholds to determine asymmetry
ASYMMETRY_THRESHOLD = 0.04  # Lower is more symmetric


def analyze_symmetry(image: np.ndarray) -> dict:
    """
    Analyze facial asymmetry and predict possible conditions.
    """
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return {"error": "No face detected."}

    landmarks = results.multi_face_landmarks[0].landmark
    h, w = image.shape[:2]

    # Calculate mirrored distances
    distances = []
    for lp, rp in zip(LEFT_POINTS, RIGHT_POINTS):
        lx, ly = int(landmarks[lp].x * w), int(landmarks[lp].y * h)
        rx, ry = int(landmarks[rp].x * w), int(landmarks[rp].y * h)
        mirrored_rx = w - rx  # mirror right side to match left
        d = np.linalg.norm(np.array([lx, ly]) - np.array([mirrored_rx, ry]))
        distances.append(d / w)  # normalize

    # Calculate average asymmetry score
    score = np.mean(distances)

    # Predict possible conditions based on threshold
    if score < 0.02:
        condition = "Very Symmetrical"
    elif score < ASYMMETRY_THRESHOLD:
        condition = "Slight Asymmetry (likely normal)"
    else:
        condition = predict_condition(landmarks, w, h)

    return {
        "asymmetry_score": round(score, 4),
        "predicted_condition": condition
    }


def predict_condition(landmarks, w, h) -> str:
    """
    Simple rule-based condition prediction based on key landmarks.
    """

    # Mouth droop: vertical difference between left and right mouth corners
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]
    mouth_diff = abs((left_mouth.y - right_mouth.y) * h)

    # Eyebrow droop: vertical difference between left and right eyebrow
    left_brow = landmarks[159]
    right_brow = landmarks[386]
    brow_diff = abs((left_brow.y - right_brow.y) * h)

    if mouth_diff > 10 and brow_diff > 8:
        return "⚠️ Possible Bell’s Palsy"
    elif mouth_diff > 10 and brow_diff < 5:
        return "⚠️ Possible Stroke"
    elif brow_diff > 12:
        return "⚠️ Possible Congenital Jaw Defect"
    else:
        return "⚠️ Facial Asymmetry Detected (Unclassified)"


def draw_landmarks(image: np.ndarray) -> np.ndarray:
    """
    Optional utility: return image with face mesh landmarks drawn.
    """
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks:
        mp_drawing = mp.solutions.drawing_utils
        annotated = image.copy()
        mp_drawing.draw_landmarks(
            annotated,
            results.multi_face_landmarks[0],
            mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
        )
        return annotated
    return image
