# analyzers.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict
from PIL import Image
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the correct base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVED_MODELS_PATH = os.path.join(BASE_DIR, "..", "saved_models")


# --- Load models safely ---
def load_safe_model(model_filename, compile=False):
    """
    Safely load a model from the correct saved_models directory
    """
    model_path = os.path.join(SAVED_MODELS_PATH, model_filename)

    # Check if file exists
    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        # Try alternative path without Frontend
        alt_path = os.path.join(BASE_DIR, "..", "..", "saved_models", model_filename)
        if os.path.exists(alt_path):
            logger.info(f"Found model at alternative path: {alt_path}")
            model_path = alt_path
        else:
            logger.error(f"Model also not found at alternative path: {alt_path}")
            return None

    try:
        # Load model with compile=False to avoid optimizer issues
        model = load_model(model_path, compile=compile)
        logger.info(f"Loaded model: {model_path}")
        return model
    except Exception as e:
        logger.error(f"Could not load {model_path}: {e}")
        return None


# Load models with correct paths and settings
age_model = load_safe_model("age_model.keras", compile=True)
gender_model = load_safe_model("gender_model.keras", compile=True)
fatigue_model = load_safe_model("best_fatigue_model.keras", compile=True)
skin_model = load_safe_model("mobilenet_skin.keras", compile=False)

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
    "Normal"
]


# --- Face Detection for preprocessing ---
def detect_face(image):
    """
    Detect face in image using Haar Cascade
    """
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            logger.warning("Haar cascade classifier not loaded properly")
            return image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            logger.info("No face detected, using entire image")
            return image

        # Return the largest face
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        x, y, w, h = faces[0]

        # Expand the face region a bit
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)

        return image[y:y + h, x:x + w]

    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return image


# --- Age & Gender ---
def predict_age_gender(image):
    """
    Predicts age (int) and gender (Male/Female) from a face image (numpy array).
    """
    if age_model is None or gender_model is None:
        logger.error("Age or gender model not loaded")
        return 30, "Unknown"

    try:
        # First try to detect and crop face
        face_image = detect_face(image)

        # Convert to PIL for consistent preprocessing
        im = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)).convert("RGB")

        # Resize to a standard size (assuming models expect 224x224)
        im_resized = im.resize((224, 224), Image.Resampling.LANCZOS)

        # Prepare for model - normalize to [0, 1]
        ar = np.asarray(im_resized).astype("float32") / 255.0
        ar = np.expand_dims(ar, axis=0)

        # Age prediction
        age_pred = age_model.predict(ar, verbose=0)
        age_pred = int(age_pred[0][0])

        # Gender prediction
        gender_pred = gender_model.predict(ar, verbose=0)[0]
        if gender_pred.shape[0] == 1:  # sigmoid output
            gender = "Male" if np.round(gender_pred[0]) == 0 else "Female"
        else:  # softmax output
            gender = gender_labels[np.argmax(gender_pred)]

        return age_pred, gender

    except Exception as e:
        logger.error(f"Age/Gender Prediction Error: {e}")
        return 30, "Unknown"


# --- Fatigue ---
def predict_fatigue(image):
    """
    Predicts fatigue status from grayscale images.
    - Model trained on 100x100 grayscale input with 2-class softmax.
    """
    if fatigue_model is None:
        logger.error("Fatigue model not loaded")
        return "Fatigue analysis unavailable"

    try:
        # Try to detect and crop face first
        face_image = detect_face(image)

        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(gray, (100, 100)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=(0, -1))  # (1,100,100,1)

        pred = fatigue_model.predict(img_expanded, verbose=0)
        label = np.argmax(pred)
        confidence = float(np.max(pred))

        if label == 1:
            return f"Fatigued ({confidence:.1%} confidence)"
        else:
            return f"Not Fatigued ({confidence:.1%} confidence)"

    except Exception as e:
        logger.error(f"Fatigue analysis error: {e}")
        return f"Fatigue analysis error: {e}"


# --- Skin Disease ---
def predict_skin_disease(image):
    """
    Predicts skin condition from close-up images.
    - Uses safe_skin_predict wrapper.
    """
    if skin_model is None:
        logger.error("Skin model not loaded")
        return "Skin analysis unavailable"

    try:
        img_resized = cv2.resize(image, (224, 224)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=0)

        # Use the safe prediction method
        pred = safe_skin_predict(skin_model, img_expanded)

        # Handle different prediction formats
        if isinstance(pred, list):
            pred = pred[0]

        label_idx = np.argmax(pred)
        label = skin_labels[label_idx] if label_idx < len(skin_labels) else "Unknown"
        confidence = float(np.max(pred)) * 100

        if confidence < 50:
            return f"Uncertain: {label} ({confidence:.1f}%)"
        elif label == "Normal":
            return f"Normal skin ({confidence:.1f}%)"
        else:
            return f"Possible {label} ({confidence:.1f}%) - Consult a dermatologist"

    except Exception as e:
        logger.error(f"Skin analysis error: {e}")
        return f"Skin analysis error: {e}"


# --- Model Status Check ---
def get_model_status():
    """
    Returns the status of all models for display in the UI
    """
    return {
        "age_model": age_model is not None,
        "gender_model": gender_model is not None,
        "fatigue_model": fatigue_model is not None,
        "skin_model": skin_model is not None
    }