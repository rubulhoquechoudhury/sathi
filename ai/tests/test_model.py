"""
Unit tests for end-to-end model training, evaluation, model loading, and local prediction.
Runs completely offline without requiring external API access.
"""

import tempfile
from pathlib import Path
import pytest
import numpy as np

from config.config import get_default_config
from preprocessing.load_jsonl import load_jsonl_dataset
from preprocessing.preprocess import PreprocessingPipeline
from models.train_xgboost import train_xgboost_baseline
from models.predict import LandslidePredictor
from models.evaluate import evaluate_predictions
from models.model_utils import compute_risk_level


def test_compute_risk_level_thresholds():
    score, level = compute_risk_level(0.10)
    assert score == 10
    assert level == "LOW"

    score, level = compute_risk_level(0.35)
    assert score == 35
    assert level == "MODERATE"

    score, level = compute_risk_level(0.65)
    assert score == 65
    assert level == "HIGH"

    score, level = compute_risk_level(0.85)
    assert score == 85
    assert level == "CRITICAL"


def test_evaluate_predictions_metrics():
    y_true = np.array([0, 1, 1, 0, 1, 0])
    y_pred_proba = np.array([0.1, 0.9, 0.8, 0.2, 0.7, 0.3])

    metrics = evaluate_predictions(y_true, y_pred_proba, threshold=0.5)

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "roc_auc" in metrics
    assert "false_negative_rate" in metrics
    assert metrics["accuracy"] == 1.0
    assert metrics["false_negative_rate"] == 0.0


def test_end_to_end_training_and_inference():
    cfg = get_default_config()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        output_models_dir = tmp_path / "saved_models"

        train_jsonl = cfg.TRAIN_JSONL
        val_jsonl = cfg.VALIDATION_JSONL

        assert train_jsonl.exists(), "Synthetic train.jsonl fixture missing."

        # Train model baseline
        train_xgboost_baseline(
            train_path=train_jsonl,
            val_path=val_jsonl,
            output_dir=output_models_dir
        )

        model_file = output_models_dir / "landslide_xgboost.json"
        schema_file = output_models_dir / "feature_schema.json"

        assert model_file.exists()
        assert schema_file.exists()

        # Test inference engine
        predictor = LandslidePredictor(model_dir=output_models_dir)

        test_records = load_jsonl_dataset(cfg.TEST_JSONL)
        assert len(test_records) > 0

        res = predictor.predict_sample(test_records[0])

        assert "landslide_probability" in res
        assert "risk_score" in res
        assert "risk_level" in res

        assert 0.0 <= res["landslide_probability"] <= 1.0
        assert 0 <= res["risk_score"] <= 100
        assert res["risk_level"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
