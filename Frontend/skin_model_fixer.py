# skin_model_fixer.py
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Lambda

def safe_skin_predict(model, img_expanded):
    """
    Try multiple input formats for the skin disease model until one works.
    This handles:
      - Single-input models
      - Two-input models (same image twice)
      - Two-input models (original + flipped)
    If all fail, returns a fallback "normal"-like prediction.
    """
    try:
        # Case 1: single input (most common)
        return model.predict(img_expanded, verbose=0)
    except Exception as e1:
        try:
            # Case 2: duplicate input for models expecting two tensors
            return model.predict([img_expanded, img_expanded], verbose=0)
        except Exception as e2:
            try:
                # Case 3: original + flipped image
                img_flipped = cv2.flip(img_expanded[0], 1)
                img_flipped = np.expand_dims(img_flipped, axis=0)
                return model.predict([img_expanded, img_flipped], verbose=0)
            except Exception as e3:
                print(f"[SkinModelFixer] All prediction methods failed: {e1}, {e2}, {e3}")
                # Return neutral prediction (last class "normal" highest)
                fallback = np.zeros((1, 10))
                fallback[0, -1] = 1.0
                return fallback