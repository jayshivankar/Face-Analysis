# analyzers.py
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from skin_model_fixer import safe_skin_predict
from PIL import Image
import traceback

# Optional: try to import mediapipe for face cropping (good to have)
try:
    import mediapipe as mp
    mp_face_detection = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4)
    HAVE_MEDIAPIPE = True
except Exception:
    HAVE_MEDIAPIPE = False

# --- Load models safely ---
def load_safe_model(path):
    try:
        model = load_model(path, compile=False)
        print(f"✅ Loaded model: {path}")
        print("    input_shape:", model.input_shape)
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

# ---- Utilities ----
def detect_and_crop_face_bgr(bgr_image):
    """Try to detect face using MediaPipe. Return cropped BGR face or original if not found."""
    if not HAVE_MEDIAPIPE:
        return bgr_image
    try:
        img_rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        results = mp_face_detection.process(img_rgb)
        if results.detections and len(results.detections) > 0:
            # take first detection
            det = results.detections[0]
            bbox = det.location_data.relative_bounding_box
            h, w = bgr_image.shape[:2]
            x_min = int(max(0, bbox.xmin * w))
            y_min = int(max(0, bbox.ymin * h))
            box_w = int(min(w - x_min, bbox.width * w))
            box_h = int(min(h - y_min, bbox.height * h))
            # expand a little
            pad_x = int(0.12 * box_w)
            pad_y = int(0.18 * box_h)
            x0 = max(0, x_min - pad_x)
            y0 = max(0, y_min - pad_y)
            x1 = min(w, x_min + box_w + pad_x)
            y1 = min(h, y_min + box_h + pad_y)
            face = bgr_image[y0:y1, x0:x1]
            if face.size == 0:
                return bgr_image
            return face
        else:
            return bgr_image
    except Exception:
        # if mediapipe errors, just return original
        return bgr_image

def _model_input_info(model):
    """Return a dict: {'ndim': 2 or 4, 'target_size': (h,w), 'channels': c} or None if model is None."""
    if model is None:
        return None
    shape = model.input_shape
    # shape could be (None, h, w, c) or (None, features)
    if isinstance(shape, list):
        # multi-input; pick first input
        shape = shape[0]
    if len(shape) == 4:
        _, h, w, c = shape
        return {"ndim": 4, "target_size": (int(h), int(w)), "channels": int(c)}
    elif len(shape) == 2:
        # flattened vector
        _, features = shape
        return {"ndim": 2, "features": int(features)}
    else:
        return {"ndim": len(shape), "raw": shape}

def _preprocess_for_model_from_bgr(bgr_image, model, grayscale=False):
    """
    Prepare numpy array suitable for model.predict:
    - bgr_image: OpenCV BGR numpy array (H,W,3)
    - model: keras model
    - grayscale: if True, convert to gray
    """
    info = _model_input_info(model)
    if info is None:
        raise ValueError("Model is None in preprocessing.")

    # If image-based model
    if info.get("ndim") == 4:
        h, w = info["target_size"]
        c = info["channels"]
        # convert color channels
        if grayscale or c == 1:
            gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY) if len(bgr_image.shape) == 3 else bgr_image
            resized = cv2.resize(gray, (w, h))
            arr = resized.astype("float32") / 255.0
            if c == 1:
                arr = np.expand_dims(arr, axis=-1)
            else:
                # if model expects 3 channels but we gave gray, duplicate
                arr = np.stack([arr]*3, axis=-1)
        else:
            # BGR -> RGB
            rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB) if bgr_image.shape[2] == 3 else cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2RGB)
            resized = cv2.resize(rgb, (w, h))
            arr = resized.astype("float32") / 255.0

        return np.expand_dims(arr, axis=0)  # (1,h,w,c)

    # If flattened model
    if info.get("ndim") == 2:
        # we will resize to a sensible shape and flatten.
        features = info["features"]
        # Choose a square size that best matches features/3
        # Try to find integer s.t. s*s*3 == features or s*s == features if grayscale
        # Prefer color flatten if divisible by 3
        if features % 3 == 0:
            s2 = features // 3
            s = int(round(np.sqrt(s2)))
            if s*s*3 == features:
                resized = cv2.resize(bgr_image, (s, s))
                arr = resized.astype("float32") / 255.0
                flat = arr.flatten().reshape(1, -1)
                return flat
        # fallback: try grayscale
        s = int(round(np.sqrt(features)))
        resized = cv2.resize(cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY), (s, s))
        arr = resized.astype("float32") / 255.0
        flat = arr.flatten().reshape(1, -1)
        return flat

    raise ValueError("Unsupported model input shape.")

# -------------------------
# Public API
# -------------------------
def predict_age_gender(image_bgr):
    """
    Accepts OpenCV BGR image (numpy array). Returns (age:int, gender:str).
    Uses face detection if available to crop to face before preprocessing.
    """
    if age_model is None or gender_model is None:
        return 30, "Unknown"

    try:
        # crop to face if possible (helps accuracy)
        face = detect_and_crop_face_bgr(image_bgr)

        # Prepare inputs depending on model expectations
        # Age may be flattened or image
        age_input = _preprocess_for_model_from_bgr(face, age_model, grayscale=False)
        gender_input = _preprocess_for_model_from_bgr(face, gender_model, grayscale=False)

        # Debug logs (prints to console)
        try:
            print("[DEBUG] age_model.input_shape:", age_model.input_shape, "-> input array shape:", age_input.shape)
            print("[DEBUG] gender_model.input_shape:", gender_model.input_shape, "-> input array shape:", gender_input.shape)
        except Exception:
            pass

        # Predict
        raw_age = age_model.predict(age_input, verbose=0)
        # handle regression output (scalar) or vector
        if np.asarray(raw_age).ndim == 2 and raw_age.shape[1] >= 1:
            age_val = float(raw_age[0][0])
        else:
            age_val = float(np.asarray(raw_age).reshape(-1)[0])
        age_pred = int(round(age_val))

        raw_gender = gender_model.predict(gender_input, verbose=0)
        raw_gender = np.asarray(raw_gender)
        # handle sigmoid (shape (1,1)) or softmax (1,n)
        if raw_gender.ndim == 2 and raw_gender.shape[1] == 1:
            gscore = float(raw_gender[0,0])
            # assume threshold 0.5 -> second label (Female) else Male
            gender = gender_labels[int(round(gscore))] if (0 <= round(gscore) <= 1) else ("Female" if gscore > 0.5 else "Male")
        else:
            idx = int(np.argmax(raw_gender, axis=1)[0])
            # guard index
            gender = gender_labels[idx] if idx < len(gender_labels) else str(idx)

        return age_pred, gender

    except Exception as e:
        print("[predict_age_gender ERROR]", e)
        traceback.print_exc()
        return 30, "Unknown"


def predict_fatigue(image_bgr):
    if fatigue_model is None:
        return "Fatigue analysis unavailable"
    try:
        # Model likely expects 100x100 grayscale; adaptive preprocessing does that
        inp = _preprocess_for_model_from_bgr(image_bgr, fatigue_model, grayscale=True)
        pred = fatigue_model.predict(inp, verbose=0)
        if pred.ndim == 2:
            label = np.argmax(pred, axis=1)[0]
            return "Fatigued" if label == 1 else "Not Fatigued"
        else:
            # fallback binary threshold
            return "Fatigued" if float(pred.reshape(-1)[0]) > 0.5 else "Not Fatigued"
    except Exception as e:
        return f"Fatigue analysis error: {e}"


def predict_skin_disease(image_bgr):
    """
    Predict skin disease. image_bgr: OpenCV BGR numpy array cropped to skin patch (close-up).
    """
    if skin_model is None:
        return "Skin analysis unavailable"
    try:
        inp = _preprocess_for_model_from_bgr(image_bgr, skin_model, grayscale=False)
        pred = safe_skin_predict(skin_model, inp)
        pred = np.asarray(pred)
        idx = int(np.argmax(pred, axis=1)[0])
        label = skin_labels[idx] if idx < len(skin_labels) else str(idx)
        confidence = float(np.max(pred)) * 100
        return f"{label} ({confidence:.1f}%)"
    except Exception as e:
        return f"Skin analysis error: {e}"
