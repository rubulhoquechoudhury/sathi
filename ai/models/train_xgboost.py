"""
XGBoost baseline model training script.
Command:
    python -m models.train_xgboost --train dataset/train.jsonl --validation dataset/validation.jsonl --output saved_models/
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

import numpy as np
import xgboost as xgb

from config.config import get_default_config, Config
from preprocessing.preprocess import PreprocessingPipeline
from preprocessing.validate_dataset import validate_dataset_file
from models.evaluate import evaluate_predictions
from models.model_utils import (
    save_xgboost_model,
    export_feature_importances
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("train_xgboost")


def train_xgboost_baseline(
    train_path: Path,
    val_path: Optional[Path],
    output_dir: Path
) -> None:
    """
    Execute full training workflow.

    Args:
        train_path: Path to train.jsonl
        val_path: Optional path to validation.jsonl
        output_dir: Output directory for saved model artifacts
    """
    cfg: Config = get_default_config()

    logger.info("=== STEP 1: VALIDATING TRAINING DATASET ===")
    train_stats = validate_dataset_file(train_path, expected_dim=cfg.ALPHAEARTH_EMBEDDING_DIM)
    logger.info(
        f"Train Dataset Stats -> Total: {train_stats['total_samples']}, Pos: {train_stats['positive']}, "
        f"Neg: {train_stats['negative']}, Pos Ratio: {train_stats['positive_ratio']:.2f}%"
    )

    logger.info("=== STEP 2: PREPROCESSING DATASET & BUILDING FEATURE MATRICES ===")
    pipeline = PreprocessingPipeline()
    X_train, y_train, train_records = pipeline.process_file(train_path)

    if X_train.shape[0] == 0 or y_train is None:
        raise ValueError(f"Training dataset at '{train_path}' contains no valid samples or labels.")

    # Calculate class weight ratio for imbalance handling
    pos_count = np.sum(y_train == 1)
    neg_count = np.sum(y_train == 0)
    scale_pos_weight = float(neg_count / pos_count) if pos_count > 0 else 1.0
    logger.info(f"Class counts -> Neg: {neg_count}, Pos: {pos_count}. Computed scale_pos_weight: {scale_pos_weight:.3f}")

    if val_path and val_path.exists():
        logger.info("=== STEP 3: PREPROCESSING VALIDATION DATASET ===")
        X_val, y_val, _ = pipeline.process_file(val_path)
    else:
        logger.warning("Validation dataset path not provided or does not exist. Skipping separate validation.")
        X_val, y_val = None, None

    logger.info("=== STEP 4: TRAINING XGBOOST CLASSIFIER ===")
    xgb_params = dict(cfg.XGB_PARAMS)
    xgb_params["scale_pos_weight"] = scale_pos_weight

    model = xgb.XGBClassifier(**xgb_params)

    if X_val is not None and y_val is not None:
        model.fit(
            X_train,
            y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            verbose=100
        )
    else:
        model.fit(X_train, y_train, verbose=True)

    logger.info("=== STEP 5: EVALUATING MODEL PERFORMANCE ===")
    eval_target_X = X_val if X_val is not None else X_train
    eval_target_y = y_val if y_val is not None else y_train

    y_pred_proba = model.predict_proba(eval_target_X)[:, 1]

    metrics_save_path = cfg.METRICS_SAVE_PATH
    metrics = evaluate_predictions(
        y_true=eval_target_y,
        y_pred_proba=y_pred_proba,
        threshold=0.5,
        output_json_path=metrics_save_path
    )

    logger.info("=== STEP 6: EXPORTING FEATURE IMPORTANCES ===")
    export_feature_importances(
        model=model,
        feature_names=pipeline.schema.feature_names,
        csv_path=cfg.FEATURE_IMPORTANCE_PATH,
        plot_path=cfg.FEATURE_IMPORTANCE_PLOT
    )

    logger.info("=== STEP 7: SAVING MODEL & FEATURE SCHEMA ===")
    output_dir.mkdir(parents=True, exist_ok=True)
    model_save_path = output_dir / "landslide_xgboost.json"
    schema_save_path = output_dir / "feature_schema.json"

    save_xgboost_model(model, model_save_path)
    pipeline.schema.save(schema_save_path)

    logger.info("SUCCESS: Training pipeline execution completed.")
    logger.info(f"Model saved to: {model_save_path}")
    logger.info(f"Schema saved to: {schema_save_path}")
    logger.info(f"Metrics saved to: {metrics_save_path}")


def main():
    cfg = get_default_config()
    parser = argparse.ArgumentParser(description="Train XGBoost Landslide Early-Warning Model")
    parser.add_argument(
        "--train",
        type=str,
        default=str(cfg.TRAIN_JSONL),
        help="Path to train.jsonl dataset"
    )
    parser.add_argument(
        "--validation",
        type=str,
        default=str(cfg.VALIDATION_JSONL),
        help="Path to validation.jsonl dataset"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(cfg.SAVED_MODELS_DIR),
        help="Output directory for saved model artifacts"
    )

    args = parser.parse_args()
    train_p = Path(args.train)
    val_p = Path(args.validation) if args.validation else None
    out_p = Path(args.output)

    if not train_p.exists():
        logger.error(f"Train dataset file not found: {train_p}")
        sys.exit(1)

    train_xgboost_baseline(
        train_path=train_p,
        val_path=val_p,
        output_dir=out_p
    )


if __name__ == "__main__":
    main()
