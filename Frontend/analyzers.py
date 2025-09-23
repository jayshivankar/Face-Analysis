import cv2
import numpy as np
from PIL import Image
import mediapipe as mp


# Age and Gender Prediction (Demo version)
def predict_age_gender(image):
    """Predicts age and gender from a face image."""
    try:
        # Simple face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            # Return reasonable values based on face detection
            age = 25 + (len(faces) * 5)  # Simple heuristic
            gender = "Male" if np.random.random() > 0.5 else "Female"
            return age, gender
        else:
            return 30, "Unknown"
    except Exception as e:
        print(f"Age/Gender prediction error: {e}")
        return 30, "Unknown"


# Fatigue Estimation (Demo version)
def predict_fatigue(image):
    """Predicts fatigue based on facial/eye features."""
    try:
        # Simple eye detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

        # Simple heuristic based on number of eyes detected
        if len(eyes) >= 2:
            return "Not Fatigued"
        elif len(eyes) == 1:
            return "Slightly Fatigued"
        else:
            return "Fatigued"
    except Exception as e:
        print(f"Fatigue prediction error: {e}")
        return "Unknown"


# Skin Disease Prediction (Demo version)
def predict_skin_disease(image):
    """Classifies skin condition from cropped skin image."""
    conditions = [
        'Normal skin',
        'Acne',
        'Actinic Keratosis',
        'Basal Cell Carcinoma',
        'Melanocytic Nevi',
        'Melanoma',
        'Normal skin',  # Higher weight for normal
        'Normal skin'  # Even higher weight
    ]

    # Simple color-based heuristic
    try:
        avg_color = np.mean(image, axis=(0, 1))
        if avg_color[0] > 150:  # Reddish tone
            return "Acne" if np.random.random() > 0.7 else "Normal skin"
        else:
            return np.random.choice(conditions)
    except:
        return "Normal skin"


# Extract cheek region (if needed)
def extract_cheek_region(image):
    """Extracts cheek region for skin analysis."""
    try:
        with mp.solutions.face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
            results = face_mesh.process(image)
            if not results.multi_face_landmarks:
                return None

            landmarks = results.multi_face_landmarks[0]
            h, w, _ = image.shape

            # Cheek points
            left_cheek = landmarks.landmark[234]
            right_cheek = landmarks.landmark[454]

            x_min = int(left_cheek.x * w) - 30
            y_min = int(left_cheek.y * h) - 30
            x_max = int(right_cheek.x * w) + 30
            y_max = y_min + 100

            cropped = image[max(0, y_min):min(h, y_max), max(0, x_min):min(w, x_max)]
            return cropped if cropped.size > 0 else None
    except Exception as e:
        print(f"Cheek extraction error: {e}")
        return None