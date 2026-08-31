"""
Feature schema metadata representation and serialization.
Tracks feature ordering, categorical encodings, and model compatibility metadata.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Union, Optional


class FeatureSchema:
    """Manages serialization and validation of feature matrices and model metadata."""

    def __init__(
        self,
        feature_names: List[str],
        categorical_mappings: Dict[str, Dict[str, int]],
        embedding_dim: int = 64,
        preprocessing_info: Optional[Dict[str, Any]] = None,
        version: str = "1.0.0"
    ) -> None:
        self.feature_names = feature_names
        self.feature_order = list(feature_names)
        self.categorical_mappings = categorical_mappings
        self.embedding_dim = embedding_dim
        self.preprocessing_info = preprocessing_info or {}
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary representation."""
        return {
            "version": self.version,
            "embedding_dim": self.embedding_dim,
            "num_features": len(self.feature_names),
            "feature_names": self.feature_names,
            "feature_order": self.feature_order,
            "categorical_mappings": self.categorical_mappings,
            "preprocessing_info": self.preprocessing_info
        }

    def save(self, file_path: Union[str, Path]) -> None:
        """Save feature schema metadata to JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "FeatureSchema":
        """Load feature schema from JSON file."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Feature schema not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            feature_names=data["feature_names"],
            categorical_mappings=data.get("categorical_mappings", {}),
            embedding_dim=data.get("embedding_dim", 64),
            preprocessing_info=data.get("preprocessing_info", {}),
            version=data.get("version", "1.0.0")
        )
