"""
Repository Classes for Database CRUD Operations.
Architectural constraint: API -> Service -> Repository -> SQLAlchemy -> DB.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database.models import (
    MonitoredLocation, Sensor, SensorReading, WeatherObservation, CitizenReport, RiskPrediction,
    DashboardStat, DistrictRiskSummary, SystemAlert, RiskTrend, ActionRecommendation
)



class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_locations(self) -> List[MonitoredLocation]:
        return self.db.query(MonitoredLocation).filter(MonitoredLocation.is_active == True).all()

    def get_by_id(self, loc_id: int) -> Optional[MonitoredLocation]:
        return self.db.query(MonitoredLocation).filter(MonitoredLocation.id == loc_id).first()

    def create(self, name: str, latitude: float, longitude: float) -> MonitoredLocation:
        loc = MonitoredLocation(name=name, latitude=latitude, longitude=longitude, is_active=True)
        self.db.add(loc)
        self.db.commit()
        self.db.refresh(loc)
        return loc


class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sensor_id(self, sensor_id: str) -> Optional[Sensor]:
        return self.db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()

    def create_sensor(self, sensor_id: str, name: str, lat: float, lon: float, sensor_type: str = "rain_gauge") -> Sensor:
        sensor = Sensor(sensor_id=sensor_id, name=name, latitude=lat, longitude=lon, sensor_type=sensor_type, is_active=True)
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def create_reading(self, sensor_id: str, rainfall_mm: float, soil_moisture: float, temp: float, humidity: float, recorded_at: Optional[datetime] = None) -> SensorReading:
        rec_time = recorded_at or datetime.now(timezone.utc)
        
        # Idempotency check: look for existing reading at exact timestamp
        existing = self.db.query(SensorReading).filter(
            SensorReading.sensor_id == sensor_id,
            SensorReading.recorded_at == rec_time
        ).first()
        if existing:
            return existing

        reading = SensorReading(
            sensor_id=sensor_id,
            rainfall_mm=rainfall_mm,
            soil_moisture=soil_moisture,
            temperature=temp,
            humidity=humidity,
            recorded_at=rec_time
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        return reading

    def get_active_sensors_with_latest_readings(self) -> List[Dict[str, Any]]:
        """
        Retrieve all active sensors and their latest reading efficiently.
        Calculates status (ONLINE, STALE, NO_DATA) based on data freshness (3600s threshold).
        Matches Phase 3 & 4 of Master Prompt.
        """
        sensors = self.db.query(Sensor).filter(Sensor.is_active == True).all()
        now_utc = datetime.now(timezone.utc)
        results = []

        for s in sensors:
            latest_reading = self.db.query(SensorReading)\
                .filter(SensorReading.sensor_id == s.sensor_id)\
                .order_by(desc(SensorReading.recorded_at))\
                .first()

            status_str = "NO_DATA"
            telemetry = {
                "temperature": None,
                "humidity": None,
                "soil_moisture": None,
                "rainfall_mm": None,
                "recorded_at": None
            }

            if latest_reading:
                rec_at = latest_reading.recorded_at
                if rec_at.tzinfo is None:
                    rec_at = rec_at.replace(tzinfo=timezone.utc)
                
                age_sec = (now_utc - rec_at).total_seconds()
                status_str = "ONLINE" if age_sec <= 3600 else "STALE"

                telemetry = {
                    "temperature": latest_reading.temperature,
                    "humidity": latest_reading.humidity,
                    "soil_moisture": latest_reading.soil_moisture,
                    "rainfall_mm": latest_reading.rainfall_mm,
                    "recorded_at": rec_at.isoformat()
                }

            results.append({
                "sensor_id": s.sensor_id,
                "location_id": s.location_id,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "sensor_type": s.sensor_type,
                "status": status_str,
                **telemetry
            })

        return results

    def get_cumulative_rainfall_windows(self, sensor_id: str, target_time: Optional[datetime] = None) -> Dict[str, float]:
        """
        Calculate true cumulative antecedent rainfall windows (1h, 24h, 3d, 7d, 14d) from historical sensor readings.
        Matches Phase 5 of Master Prompt.
        """
        ref_time = target_time or datetime.now(timezone.utc)

        def _sum_window(hours: float) -> float:
            start_t = ref_time - timedelta(hours=hours)
            res = self.db.query(func.coalesce(func.sum(SensorReading.rainfall_mm), 0.0)).filter(
                SensorReading.sensor_id == sensor_id,
                SensorReading.recorded_at >= start_t,
                SensorReading.recorded_at <= ref_time
            ).scalar()
            return float(res)

        r_1h = _sum_window(1)
        r_24h = _sum_window(24)
        r_3d = _sum_window(72)
        r_7d = _sum_window(168)
        r_14d = _sum_window(336)

        # Enforce physical monotonicity: 14d >= 7d >= 3d >= 24h >= 1h
        r_24h = max(r_24h, r_1h)
        r_3d = max(r_3d, r_24h)
        r_7d = max(r_7d, r_3d)
        r_14d = max(r_14d, r_7d)

        return {
            "rain_1h": round(r_1h, 2),
            "rain_24h": round(r_24h, 2),
            "rain_3d": round(r_3d, 2),
            "rain_7d": round(r_7d, 2),
            "rain_14d": round(r_14d, 2)
        }



class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_observation(self, data: Dict[str, Any]) -> WeatherObservation:
        obs = WeatherObservation(
            latitude=data["latitude"],
            longitude=data["longitude"],
            rain_1h=data.get("rain_1h", 0.0),
            rain_24h=data.get("rain_24h", 0.0),
            rain_3d=data.get("rain_3d", 0.0),
            rain_7d=data.get("rain_7d", 0.0),
            rain_14d=data.get("rain_14d", 0.0),
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            soil_moisture=data.get("soil_moisture"),
            observed_at=data.get("observed_at", datetime.now(timezone.utc))
        )
        self.db.add(obs)
        self.db.commit()
        self.db.refresh(obs)
        return obs

    def get_latest_near(self, lat: float, lon: float) -> Optional[WeatherObservation]:
        return self.db.query(WeatherObservation).order_by(desc(WeatherObservation.observed_at)).first()


class CitizenReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_report(self, lat: float, lon: float, severity: int, description: str, image_url: Optional[str] = None) -> CitizenReport:
        rep = CitizenReport(latitude=lat, longitude=lon, severity=severity, description=description, image_url=image_url)
        self.db.add(rep)
        self.db.commit()
        self.db.refresh(rep)
        return rep

    def get_all(self, limit: int = 50) -> List[CitizenReport]:
        return self.db.query(CitizenReport).order_by(desc(CitizenReport.created_at)).limit(limit).all()


class RiskPredictionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Dict[str, Any]) -> RiskPrediction:
        pred = RiskPrediction(
            location_id=data.get("location_id"),
            latitude=data["latitude"],
            longitude=data["longitude"],
            landslide_probability=data["risk_probability"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            data_status=data.get("data_status", "ALPHAEARTH_UNAVAILABLE"),
            model_version=data.get("model_version", "xgb-v1"),
            prediction_timestamp=data.get("prediction_timestamp", datetime.now(timezone.utc))
        )
        self.db.add(pred)
        self.db.commit()
        self.db.refresh(pred)
        return pred

    def get_latest_predictions_all_locations(self) -> List[RiskPrediction]:
        subquery = self.db.query(
            RiskPrediction.latitude,
            RiskPrediction.longitude,
            func.max(RiskPrediction.prediction_timestamp).label("max_time")
        ).group_by(RiskPrediction.latitude, RiskPrediction.longitude).subquery()

        query = self.db.query(RiskPrediction).join(
            subquery,
            (RiskPrediction.latitude == subquery.c.latitude) &
            (RiskPrediction.longitude == subquery.c.longitude) &
            (RiskPrediction.prediction_timestamp == subquery.c.max_time)
        )
        return query.all()

    def get_history(self, limit: int = 100) -> List[RiskPrediction]:
        return self.db.query(RiskPrediction).order_by(desc(RiskPrediction.prediction_timestamp)).limit(limit).all()


class DashboardRepository:
    """Repository for querying operational dashboard metrics."""

    def __init__(self, db: Session):
        self.db = db

    def get_stats(self) -> List[DashboardStat]:
        return self.db.query(DashboardStat).all()

    def get_district_summaries(self) -> List[DistrictRiskSummary]:
        return self.db.query(DistrictRiskSummary).order_by(desc(DistrictRiskSummary.landslide_risk_pct)).all()

    def get_active_alerts(self, limit: int = 10) -> List[SystemAlert]:
        return self.db.query(SystemAlert).filter(SystemAlert.is_active == True).order_by(desc(SystemAlert.created_at)).limit(limit).all()

    def get_risk_trends(self) -> List[RiskTrend]:
        return self.db.query(RiskTrend).order_by(RiskTrend.day_order.asc()).all()

    def get_active_recommendations(self) -> List[ActionRecommendation]:
        return self.db.query(ActionRecommendation).filter(ActionRecommendation.is_active == True).order_by(ActionRecommendation.priority.asc()).all()

    def create_alert(self, alert_type: str, title: str, description: str, severity: str, time_ago: str = "Just now") -> SystemAlert:
        alert = SystemAlert(
            alert_type=alert_type,
            title=title,
            description=description,
            severity=severity,
            time_ago=time_ago,
            is_active=True
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def create_recommendation(self, recommendation_text: str, priority: int = 1) -> ActionRecommendation:
        rec = ActionRecommendation(
            recommendation_text=recommendation_text,
            priority=priority,
            is_active=True
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec


