import cv2
import numpy as np
from tensorflow.keras.models import load_model


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