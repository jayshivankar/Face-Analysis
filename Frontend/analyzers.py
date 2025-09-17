# analyzers.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict
from PIL import Image
import os


# --- Load models safely ---
def load_safe_model(path, compile=True):
    try:
        # Check if model file exists
        if not os.path.exists(path):
            print(f"❌ Model file not found: {path}")
            return None

        model = load_model(path, compile=compile)
        print(f"✅ Loaded model: {path} | Inputs: {model.input_shape}")
        return model
    except Exception as e:
        print(f"⚠️ Could not load {path}: {e}")
        return None


# Load models with absolute paths to avoid relative path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
age_model = load_safe_model(os.path.join(BASE_DIR, "saved_models", "age_model.keras"))
gender_model = load_safe_model(os.path.join(BASE_DIR, "saved_models", "gender_model.keras"))
fatigue_model = load_safe_model(os.path.join(BASE_DIR, "saved_models", "best_fatigue_model.keras"))
skin_model = load_safe_model(os.path.join(BASE_DIR, "saved_models", "mobilenet_skin.keras"), compile=False)

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
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

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


# --- Age & Gender ---
def predict_age_gender(image):
    """
    Predicts age (int) and gender (Male/Female) from a face image (numpy array).
    """
    if age_model is None or gender_model is None:
        return 30, "Unknown"

    try:
        # First try to detect and crop face
        face_image = detect_face(image)
        if face_image is None:
            face_image = image  # Use the whole image if no face detected

        # Convert to PIL for consistent preprocessing
        im = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)).convert("RGB")

        # Center square crop
        width, height = im.size
        if width != height:
            size = min(width, height)
            left = (width - size) / 2
            top = (height - size) / 2
            right = (width + size) / 2
            bottom = (height + size) / 2
            im = im.crop((left, top, right, bottom))

        # Resize to model input
        im_resized = im.resize((224, 224), Image.Resampling.LANCZOS)

        # Prepare for model
        ar = np.asarray(im_resized).astype("float32") / 255.0
        ar = np.expand_dims(ar, axis=0)

        # Age prediction
        age_pred = int(age_model.predict(ar, verbose=0)[0][0])

        # Gender prediction
        gender_pred = gender_model.predict(ar, verbose=0)[0]
        if gender_pred.shape[0] == 1:  # sigmoid
            gender = "Male" if np.round(gender_pred[0]) == 0 else "Female"
        else:  # softmax
            gender = gender_labels[np.argmax(gender_pred)]

        return age_pred, gender

    except Exception as e:
        print(f"[Age/Gender Prediction Error] {e}")
        return 30, "Unknown"


# --- Fatigue ---
def predict_fatigue(image):
    """
    Predicts fatigue status from grayscale images.
    - Model trained on 100x100 grayscale input with 2-class softmax.
    """
    if fatigue_model is None:
        return "Fatigue analysis unavailable"

    try:
        # Try to detect and crop face first
        face_image = detect_face(image)
        if face_image is None:
            face_image = image

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
        return f"Fatigue analysis error: {e}"


# --- Skin Disease ---
def predict_skin_disease(image):
    """
    Predicts skin condition from close-up images.
    - Handles both single-input and two-input MobileNet models.
    - Uses safe_skin_predict wrapper.
    """
    if skin_model is None:
        return "Skin analysis unavailable"

    try:
        img_resized = cv2.resize(image, (224, 224)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=0)

        pred = safe_skin_predict(skin_model, img_expanded)
        label = skin_labels[np.argmax(pred)]
        confidence = float(np.max(pred)) * 100

        if confidence < 50:
            return f"Uncertain: {label} ({confidence:.1f}%)"
        elif label == "Normal":
            return f"Normal skin ({confidence:.1f}%)"
        else:
            return f"Possible {label} ({confidence:.1f}%) - Consult a dermatologist"

    except Exception as e:
        return f"Skin analysis error: {e}"