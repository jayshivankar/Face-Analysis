import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict

# Load models safely
def try_load(path):
    try:
        return load_model(path)
    except Exception as e:
        print(f"[Model Load Error] {path}: {e}")
        return None

age_model = try_load("saved_models/age_model.keras")
gender_model = try_load("saved_models/gender_model.keras")
fatigue_model = try_load("saved_models/best_fatigue_model.keras")
skin_model = try_load("saved_models/mobilenet_skin.keras")

gender_labels = ["Male", "Female"]
skin_labels = [
    "Acne",
    "Actinic Keratosis",
    "Basal Cell Carcinoma",
    "Dermatofibroma",
    "Melanocytic Nevi",
    "Melanoma",
    "Seborrheic Keratoses",
    "Squamous Cell Carcinoma",
    "Vascular Lesion",
    "normal",
]

# --- Age & Gender ---
def predict_age_gender(image):
    age_pred, gender_label = 30, "Unknown"
    try:
        img = cv2.resize(image, (224, 224)) / 255.0
        img = np.expand_dims(img, axis=0)

        if age_model:
            age_pred = age_model.predict(img, verbose=0)[0][0]

        if gender_model:
            gender_pred = gender_model.predict(img, verbose=0)
            gender_label = gender_labels[np.argmax(gender_pred)]
    except Exception as e:
        print(f"[Age/Gender Error] {e}")
    return int(age_pred), gender_label

# --- Fatigue ---
def predict_fatigue(image):
    if not fatigue_model:
        return "Fatigue analysis unavailable"
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
        img = cv2.resize(gray, (96, 96)) / 255.0
        if len(fatigue_model.input_shape) == 2:
            pred = fatigue_model.predict(img.flatten().reshape(1, -1), verbose=0)
        else:
            pred = fatigue_model.predict(np.expand_dims(img, (0, -1)), verbose=0)
        return "Fatigued" if pred[0][0] > 0.5 else "Not Fatigued"
    except Exception as e:
        return f"Fatigue analysis error: {e}"

# --- Skin Disease ---
def predict_skin_disease(image):
    if not skin_model:
        return "Skin analysis unavailable"
    try:
        img = cv2.resize(image, (224, 224)) / 255.0
        img = np.expand_dims(img, axis=0)
        pred = safe_skin_predict(skin_model, img)
        return skin_labels[int(np.argmax(pred))]
    except Exception as e:
        return f"Skin analysis error: {e}"

