import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp



# Age and Gender Prediction

age_model = load_model("saved_models/age_model.keras")
gender_model = load_model("saved_models/gender_model.keras")
gender_labels = ["Male","Female"]

def predict_age_gender(image):
    """Predicts age and gender from a face image."""
    img_resized = cv2.resize(image,(224,224))/255.0
    img_expanded = np.expand_dims(img_resized,axis=0)

    age_pred = age_model.predict(img_expanded)[0][0]
    gender_pred = gender_model.predict(img_expanded)
    gender_label = gender_labels[np.argmax(gender_pred)]

    return int(age_pred),gender_pred

# Fatigue Estimation

fatigue_model = load_model("saved_models/best_fatigue_model.keras")


def predict_fatigue(image):
    """Predicts fatigue based on facial/eye features."""
    img_resized = cv2.resize(image, (224, 224)) / 255.0
    img_expanded = np.expand_dims(img_resized, axis=0)

    pred = fatigue_model.predict(img_expanded)
    return "Fatigued" if pred[0][0] > 0.5 else "Not Fatigued"

# Extract face image

mp_face_mesh = mp.solutions.face_mesh

def extract_cheek_region(image):
    """Extracts cheek region for skin analysis."""
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(image)
        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0]
        h, w, _ = image.shape

        # Example: Use cheek points (MP landmark IDs)
        left_cheek_point = landmarks.landmark[234]
        right_cheek_point = landmarks.landmark[454]

        x_min = int(left_cheek_point.x * w) - 30
        y_min = int(left_cheek_point.y * h) - 30
        x_max = int(right_cheek_point.x * w) + 30
        y_max = y_min + 100  # fixed height

        cropped = image[max(0, y_min):min(h, y_max), max(0, x_min):min(w, x_max)]
        if cropped.size == 0:
            return None
        return cropped

# Skin Disease

skin_model = load_model("saved_models/mobilenet_skin.keras")
skin_labels = [
    'Acne',
    'Actinic Keratosis',
    'Basal Cell Carcinoma ',
    'Dermatofibroma',
    'Melanocytic Nevi ',
    'Melanoma',
    'Seborrheic Keratoses',
    'Squamous Cell Carcinoma ',
    'Vascular Lesion',
    'normal'
]


def predict_skin_disease(image):
    """Classifies skin condition from cropped skin image."""
    img_resized = cv2.resize(image, (224, 224)) / 255.0
    img_expanded = np.expand_dims(img_resized, axis=0)

    pred = skin_model.predict(img_expanded)
    label = skin_labels[np.argmax(pred)]
    return label