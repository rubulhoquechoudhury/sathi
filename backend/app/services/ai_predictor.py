"""
AI Prediction Service interfacing with the trained XGBoost model and feature schema.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

# Ensure ai directory (which contains models, preprocessing, config) is on sys.path
ai_dir = str(settings.ROOT_DIR / "ai")
if ai_dir not in sys.path:
    sys.path.insert(0, ai_dir)

try:
    from models.predict import LandslidePredictor
    MODEL_ENGINE_AVAILABLE = True
except ImportError as err:
    logger.warning(f"Could not import AI prediction engine from ai module: {err}")
    LandslidePredictor = None
    MODEL_ENGINE_AVAILABLE = False


class AIPredictionService:
    """Singleton service wrapper for loading model artifacts and generating predictions."""

    _instance: Optional["AIPredictionService"] = None

    def __init__(self, model_dir: Optional[Path] = None) -> None:
        self.model_dir = model_dir or settings.AI_MODEL_DIR
        self.predictor: Optional[LandslidePredictor] = None
        self.is_loaded = False
        self.load_error: Optional[str] = None
        self._load_model()

    def _load_model(self) -> None:
        """Attempt to load trained XGBoost model and feature schema."""
        if not MODEL_ENGINE_AVAILABLE:
            self.load_error = "AI model import dependencies missing."
            return

        try:
            if not self.model_dir.exists():
                self.load_error = f"Model directory does not exist: {self.model_dir}"
                logger.warning(self.load_error)
                return

            self.predictor = LandslidePredictor(model_dir=self.model_dir)
            self.is_loaded = True
            logger.info(f"AIPredictionService loaded model successfully from {self.model_dir}")
        except Exception as err:
            self.load_error = str(err)
            logger.error(f"Failed to load AI model from {self.model_dir}: {err}")

    def predict(self, record_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate landslide risk prediction for sample dict.

        Args:
            record_dict: Dictionary payload matching schema.

        Returns:
            Dictionary containing landslide_probability, risk_score, and risk_level.
        """
        if not self.is_loaded or self.predictor is None:
            raise RuntimeError(f"AI Model is not loaded. Details: {self.load_error}")

        return self.predictor.predict_sample(record_dict)


# Global Singleton Instance
_service_instance: Optional[AIPredictionService] = None


def get_ai_predictor() -> AIPredictionService:
    """Dependency injection helper returning singleton AIPredictionService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = AIPredictionService()
    return _service_instance
