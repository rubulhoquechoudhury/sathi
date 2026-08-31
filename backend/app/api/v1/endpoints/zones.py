"""
Risk Zones API endpoint providing spatial risk polygon layers computed with the AI model.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from app.services.ai_predictor import get_ai_predictor, AIPredictionService

router = APIRouter()


# Multi-level risk zone polygons covering North-East India region
SPATIAL_ZONES = [
    {
        "id": "zone-critical-1",
        "name": "Guwahati Ridge & South Slope",
        "type": "landslide",
        "coordinates": [
            [26.14, 91.70],
            [26.18, 91.75],
            [26.15, 91.82],
            [26.10, 91.78],
            [26.11, 91.71]
        ],
        "sample_location": {"latitude": 26.15, "longitude": 91.75},
        "sample_terrain": {"elevation": 2100.0, "slope": 44.5, "twi": 9.2},
        "sample_rainfall": {"rain_1h": 35.0, "rain_24h": 125.0, "rain_3d": 210.0, "rain_7d": 380.0, "rain_14d": 520.0}
    },
    {
        "id": "zone-high-1",
        "name": "Meghalaya Foothills – North Slope",
        "type": "landslide",
        "coordinates": [
            [25.98, 91.82],
            [26.02, 91.90],
            [25.99, 91.96],
            [25.93, 91.92],
            [25.94, 91.84]
        ],
        "sample_location": {"latitude": 25.98, "longitude": 91.82},
        "sample_terrain": {"elevation": 1820.4, "slope": 38.7, "twi": 8.4},
        "sample_rainfall": {"rain_1h": 22.2, "rain_24h": 94.5, "rain_3d": 182.2, "rain_7d": 310.1, "rain_14d": 450.3}
    },
    {
        "id": "zone-moderate-1",
        "name": "Ri-Bhoi Hill Slopes",
        "type": "landslide",
        "coordinates": [
            [25.90, 91.65],
            [25.95, 91.72],
            [25.93, 91.80],
            [25.87, 91.78],
            [25.86, 91.69]
        ],
        "sample_location": {"latitude": 25.90, "longitude": 91.65},
        "sample_terrain": {"elevation": 1450.0, "slope": 28.4, "twi": 6.8},
        "sample_rainfall": {"rain_1h": 14.0, "rain_24h": 65.0, "rain_3d": 130.0, "rain_7d": 220.0, "rain_14d": 340.0}
    },
    {
        "id": "zone-low-1",
        "name": "Dispur Valley Settlement",
        "type": "landslide",
        "coordinates": [
            [26.12, 91.78],
            [26.16, 91.83],
            [26.13, 91.89],
            [26.09, 91.85],
            [26.09, 91.79]
        ],
        "sample_location": {"latitude": 26.12, "longitude": 91.78},
        "sample_terrain": {"elevation": 650.0, "slope": 8.2, "twi": 3.2},
        "sample_rainfall": {"rain_1h": 0.0, "rain_24h": 2.1, "rain_3d": 5.4, "rain_7d": 12.0, "rain_14d": 25.0}
    },
    {
        "id": "zone-flood-1",
        "name": "Brahmaputra Floodplain – West",
        "type": "flood",
        "coordinates": [
            [26.22, 91.55],
            [26.28, 91.62],
            [26.25, 91.72],
            [26.18, 91.70],
            [26.15, 91.60]
        ],
        "sample_location": {"latitude": 26.22, "longitude": 91.55},
        "sample_terrain": {"elevation": 55.0, "slope": 2.1, "twi": 11.2},
        "sample_rainfall": {"rain_1h": 5.0, "rain_24h": 40.0, "rain_3d": 80.0, "rain_7d": 150.0, "rain_14d": 220.0}
    }
]


@router.get("/zones", response_model=List[Dict[str, Any]])
def get_risk_zones(
    ai_service: AIPredictionService = Depends(get_ai_predictor)
) -> List[Dict[str, Any]]:
    """
    Get dynamic spatial risk zones evaluated with the trained AI model.
    """
    results = []

    for zone in SPATIAL_ZONES:
        zone_data = dict(zone)

        if ai_service.is_loaded:
            try:
                payload = {
                    "location": zone["sample_location"],
                    "terrain": zone["sample_terrain"],
                    "rainfall": zone["sample_rainfall"]
                }
                pred = ai_service.predict(payload)
                zone_data["landslide_probability"] = pred["landslide_probability"]
                zone_data["risk_score"] = pred["risk_score"]
                zone_data["risk_level"] = pred["risk_level"]
            except Exception:
                zone_data["risk_level"] = "UNKNOWN"

        results.append(zone_data)

    return results
