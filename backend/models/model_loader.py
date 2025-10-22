import os
import logging
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self):
        self.models_dir = Path(__file__).parent.parent.parent / "saved_models"
        self.age_model = None
        self.gender_model = None
        self.fatigue_model = None
        self.skin_model = None

        self.load_all_models()

    def load_all_models(self):
        try:
            age_path = self.models_dir / "age_model.keras"
            if age_path.exists():
                self.age_model = keras.models.load_model(str(age_path))
                logger.info("Age model loaded successfully")
            else:
                logger.warning(f"Age model not found at {age_path}")
        except Exception as e:
            logger.error(f"Failed to load age model: {e}")

        try:
            gender_path = self.models_dir / "gender_model.keras"
            if gender_path.exists():
                self.gender_model = keras.models.load_model(str(gender_path))
                logger.info("Gender model loaded successfully")
            else:
                logger.warning(f"Gender model not found at {gender_path}")
        except Exception as e:
            logger.error(f"Failed to load gender model: {e}")

        try:
            fatigue_path = self.models_dir / "best_fatigue_model.keras"
            if fatigue_path.exists():
                self.fatigue_model = keras.models.load_model(str(fatigue_path))
                logger.info("Fatigue model loaded successfully")
            else:
                logger.warning(f"Fatigue model not found at {fatigue_path}")
        except Exception as e:
            logger.error(f"Failed to load fatigue model: {e}")

        try:
            skin_path = self.models_dir / "mobilenet_skin.keras"
            if skin_path.exists():
                self.skin_model = keras.models.load_model(str(skin_path))
                logger.info("Skin model loaded successfully")
            else:
                logger.warning(f"Skin model not found at {skin_path}")
        except Exception as e:
            logger.error(f"Failed to load skin model: {e}")

    def get_model_status(self):
        return {
            "age_model": "loaded" if self.age_model else "not_loaded",
            "gender_model": "loaded" if self.gender_model else "not_loaded",
            "fatigue_model": "loaded" if self.fatigue_model else "not_loaded",
            "skin_model": "loaded" if self.skin_model else "not_loaded"
        }
