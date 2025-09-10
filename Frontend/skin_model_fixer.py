import cv2
import numpy as np

def safe_skin_predict(model, img_expanded):
    """
    Tries different input formats to make skin model prediction work.
    """
    try:
        return model.predict(img_expanded, verbose=0)
    except ValueError:
        try:
            # Try duplicate input
            return model.predict([img_expanded, img_expanded], verbose=0)
        except ValueError:
            # Try flipped second input
            img_flipped = cv2.flip(img_expanded[0], 1)
            img_flipped_expanded = np.expand_dims(img_flipped, axis=0)
            return model.predict([img_expanded, img_flipped_expanded], verbose=0)
