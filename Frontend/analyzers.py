import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict
from PIL import Image

# --- Load models safely ---
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

# --- Age & Gender ---
def predict_age_gender(image):
    """
    Predicts age (int) and gender (Male/Female) from a face image (numpy array).
    """
    if age_model is None or gender_model is None:
        return 30, "Unknown"

    try:
        # Convert NumPy -> PIL for consistent preprocessing
        im = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).convert("RGB")

        # Center square crop
        width, height = im.size
        if width != height:
            if width > height:
                left = (width - height) / 2
                right = left + height
                im = im.crop((left, 0, right, height))
            else:
                top = (height - width) / 2
                bottom = top + width
                im = im.crop((0, top, width, bottom))

        # Resize to model input
        im_resized = im.resize((224, 224), Image.Resampling.LANCZOS)

        # Prepare for model
        ar = np.asarray(im_resized).astype("float32") / 255.0
        ar = np.expand_dims(ar, axis=0)

        # Age
        age_pred = int(age_model.predict(ar, verbose=0)[0][0])

        # Gender
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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(gray, (100, 100)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=(0, -1))  # (1,100,100,1)

        pred = fatigue_model.predict(img_expanded, verbose=0)
        label = np.argmax(pred)
        return "Fatigued" if label == 1 else "Not Fatigued"

    except Exception as e:
        return f"Fatigue analysis error: {e}"


# --- Skin Disease ---
def predict_skin_disease(image):
    """
    Predicts skin condition from close-up images.
    - Model trained on 224x224 RGB input (MobileNet backbone).
    - Uses safe_skin_predict to handle multi-input cases.
    """
    if skin_model is None:
        return "Skin analysis unavailable"

    try:
        img_resized = cv2.resize(image, (224, 224)) / 255.0
        img_expanded = np.expand_dims(img_resized, axis=0)

        pred = safe_skin_predict(skin_model, img_expanded)
        label = skin_labels[np.argmax(pred)]
        confidence = float(np.max(pred)) * 100
        return f"{label} ({confidence:.1f}%)"

    except Exception as e:
        return f"Skin analysis error: {e}"
