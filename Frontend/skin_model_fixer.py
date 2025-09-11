import cv2
import numpy as np

def safe_skin_predict(model, img_expanded):
    """
    Tries multiple input formats for skin disease model.
    """
    try:
        return model.predict(img_expanded, verbose=0)
    except ValueError:
        try:
            # Duplicate input
            return model.predict([img_expanded, img_expanded], verbose=0)
        except ValueError:
            try:
                # Flipped second input
                img_flipped = cv2.flip(img_expanded[0], 1)
                img_flipped = np.expand_dims(img_flipped, axis=0)
                return model.predict([img_expanded, img_flipped], verbose=0)
            except Exception as e:
                print(f"[Skin Prediction Error] {e}")
                return np.zeros((1, 10))  # fallback: "normal"
