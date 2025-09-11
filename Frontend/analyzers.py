import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict

# --- Load models with safe fallbacks ---
def load_safe_model(path):
    try:
        model = load_model(path)
        print(f"✅ Loaded model: {path}")
        return model
    except Exception as e:
        print(f"⚠️ Could not load {path}: {e}")
        return None

age_model = load_safe_model("saved_models/age_model.keras")
gender_model = load_safe_model("saved_models/gender_model.keras")
fatigue_model = load_safe_model("saved_models/best_fatigue_model.keras")
skin_model = load_safe_model("saved_models/mobilenet_skin.keras")

# --- Labels ---
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
    "normal"
]

# --- Age & Gender ---
def predict_age_gender(image):
    age_pred, gender_label = 30, "Unknown"
    try:
        # Default resize
        target_size = (224, 224)
        img_resized = cv2.resize(image, target_size) / 255.0

        # --- Age prediction ---
        if age_model:
            if len(age_model.input_shape) == 2:  # expects flat input
                flat = img_resized.flatten().reshape(1, -1)
                age_pred = age_model.predict(flat, verbose=0)[0][0]
            else:  # CNN input
                img_expanded = np.expand_dims(img_resized, axis=0)
                age_pred = age_model.predict(img_expanded, verbose=0)[0][0]

        # --- Gender prediction ---
        if gender_model:
            if len(gender_model.input_shape) == 2:  # expects flat input
                flat = img_resized.flatten().reshape(1, -1)
                gender_pred = gender_model.predict(flat, verbose=0)
            else:
                img_expanded = np.expand_dims(img_resized, axis=0)
                gender_pred = gender_model.predict(img_expanded, verbose=0)

            gender_label = gender_labels[np.argmax(gender_pred)]

    except Exception as e:
        print(f"[Age/Gender Prediction Error] {e}")

    return int(age_pred), gender_label


# --- Fatigue ---
def predict_fatigue(image):
    if fatigue_model is None:
        return "Fatigue analysis unavailable"

    try:
        # Convert to grayscale if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        img_resized = cv2.resize(gray, (96, 96)) / 255.0

        if len(fatigue_model.input_shape) == 2:  # Flattened input
            flattened = img_resized.flatten().reshape(1, -1)
            pred = fatigue_model.predict(flattened, verbose=0)
        else:  # CNN input
            img_expanded = np.expand_dims(img_resized, axis=(0, -1))
            pred = fatigue_model.predict(img_expanded, verbose=0)

        return "Fatigued" if pred[0][0] > 0.5 else "Not Fatigued"
    except Exception as e:
        return f"Fatigue analysis error: {e}"

# --- Skin Disease ---
def predict_skin_disease(image):
    if skin_model is None:
        return "Skin analysis unavailable"

    try:
        img_resized = cv2.resize(image, (224, 224)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=0)

        pred = safe_skin_predict(skin_model, img_expanded)
        label = skin_labels[np.argmax(pred)]
        return label
    except Exception as e:
        return f"Skin analysis error: {e}"
