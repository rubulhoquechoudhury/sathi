"""
Initial Data Seeder for SATHI Landslide & Flood Monitoring Operations.
Populates initial operational records into SQL database upon startup if tables are empty.
"""

import logging
from sqlalchemy.orm import Session
from app.database.models import (
    MonitoredLocation, Sensor, DashboardStat, DistrictRiskSummary,
    SystemAlert, RiskTrend, ActionRecommendation
)

logger = logging.getLogger(__name__)


def seed_initial_data(db: Session) -> None:
    """Populate default operational dashboard data and monitored locations if empty."""
    try:
        # 1. Monitored Locations
        if db.query(MonitoredLocation).count() == 0:
            locations = [
                MonitoredLocation(name="Guwahati Ridge & South Slope", latitude=26.15, longitude=91.75),
                MonitoredLocation(name="Shillong Ridge & Cherrapunji Foothills", latitude=25.55, longitude=91.90),
                MonitoredLocation(name="Itanagar Hills Slopes", latitude=27.08, longitude=93.65),
                MonitoredLocation(name="Gangtok Ridge & Teesta Gorge", latitude=27.33, longitude=88.62),
                MonitoredLocation(name="Ukhrul Border Slopes", latitude=24.82, longitude=93.95),
                MonitoredLocation(name="Aizawl Steep Ridge", latitude=23.73, longitude=92.72),
                MonitoredLocation(name="Kohima Town Slopes", latitude=25.65, longitude=94.10),
                MonitoredLocation(name="Jampui Hills Ridge", latitude=23.83, longitude=91.28)
            ]
            db.add_all(locations)
            db.commit()
            logger.info(f"Seeded {len(locations)} MonitoredLocations.")

        # 2. IoT Sensors
        if db.query(Sensor).count() == 0:
            sensors = [
                Sensor(sensor_id="SENSOR_GUWAHATI", name="Guwahati Station", latitude=26.15, longitude=91.75, sensor_type="rain_gauge"),
                Sensor(sensor_id="SENSOR_SHILLONG", name="Shillong Station", latitude=25.55, longitude=91.90, sensor_type="rain_gauge"),
                Sensor(sensor_id="SENSOR_ITANAGAR", name="Itanagar Station", latitude=27.08, longitude=93.65, sensor_type="piezometer"),
                Sensor(sensor_id="SENSOR_GANGTOK", name="Gangtok Station", latitude=27.33, longitude=88.62, sensor_type="inclinometer"),
                Sensor(sensor_id="SENSOR_UKHRUL", name="Ukhrul Station", latitude=24.82, longitude=93.95, sensor_type="rain_gauge"),
                Sensor(sensor_id="SENSOR_AIZAWL", name="Aizawl Station", latitude=23.73, longitude=92.72, sensor_type="inclinometer"),
                Sensor(sensor_id="SENSOR_KOHIMA", name="Kohima Station", latitude=25.65, longitude=94.10, sensor_type="rain_gauge"),
                Sensor(sensor_id="SENSOR_JAMPUI", name="Jampui Station", latitude=23.83, longitude=91.28, sensor_type="rain_gauge")
            ]
            db.add_all(sensors)
            db.commit()
            logger.info(f"Seeded {len(sensors)} Sensors.")

        # 3. Dashboard Stats
        if db.query(DashboardStat).count() == 0:
            stats = [
                DashboardStat(stat_key="flood_alerts", label="Flood alerts", value="12", delta="+3 since yesterday", tone="flood"),
                DashboardStat(stat_key="landslide_watch", label="Landslide watch", value="08", delta="+2 high-priority zones", tone="landslide"),
                DashboardStat(stat_key="people_at_risk", label="People at risk", value="2.4K", delta="Across 6 districts", tone="risk"),
                DashboardStat(stat_key="rainfall_forecast", label="Rainfall forecast", value="62 mm", delta="24h cumulative", tone="rain")
            ]
            db.add_all(stats)
            db.commit()
            logger.info("Seeded DashboardStats.")

        # 4. District Risk Summaries
        if db.query(DistrictRiskSummary).count() == 0:
            summaries = [
                DistrictRiskSummary(district="Kamrup", state="Assam", flood_risk_pct=78.0, landslide_risk_pct=42.0, status="Moderate", people_at_risk=450),
                DistrictRiskSummary(district="Goalpara", state="Assam", flood_risk_pct=88.0, landslide_risk_pct=55.0, status="High", people_at_risk=620),
                DistrictRiskSummary(district="Dima Hasao", state="Assam", flood_risk_pct=46.0, landslide_risk_pct=83.0, status="Critical", people_at_risk=810),
                DistrictRiskSummary(district="Karbi Anglong", state="Assam", flood_risk_pct=62.0, landslide_risk_pct=71.0, status="High", people_at_risk=390),
                DistrictRiskSummary(district="West Khasi Hills", state="Meghalaya", flood_risk_pct=39.0, landslide_risk_pct=90.0, status="Critical", people_at_risk=540)
            ]
            db.add_all(summaries)
            db.commit()
            logger.info("Seeded DistrictRiskSummaries.")

        # 5. System Alerts
        if db.query(SystemAlert).count() == 0:
            alerts = [
                SystemAlert(
                    alert_type="Flood",
                    title="Brahmaputra basin surge",
                    description="River level above seasonal average near Kamrup and Goalpara.",
                    severity="High",
                    time_ago="10 mins ago"
                ),
                SystemAlert(
                    alert_type="Landslide",
                    title="Slope instability alert",
                    description="Heavy rain and loose soil detected in Dima Hasao foothills.",
                    severity="Critical",
                    time_ago="28 mins ago"
                ),
                SystemAlert(
                    alert_type="Rainfall",
                    title="Monsoon intensity watch",
                    description="Persistent rainfall is increasing runoff in the eastern hill belts.",
                    severity="Moderate",
                    time_ago="1 hr ago"
                )
            ]
            db.add_all(alerts)
            db.commit()
            logger.info("Seeded SystemAlerts.")

        # 6. Risk Trends (7 days)
        if db.query(RiskTrend).count() == 0:
            trends = [
                RiskTrend(day_label="Mon", day_order=1, risk_value=42.0),
                RiskTrend(day_label="Tue", day_order=2, risk_value=56.0),
                RiskTrend(day_label="Wed", day_order=3, risk_value=60.0),
                RiskTrend(day_label="Thu", day_order=4, risk_value=74.0),
                RiskTrend(day_label="Fri", day_order=5, risk_value=68.0),
                RiskTrend(day_label="Sat", day_order=6, risk_value=86.0),
                RiskTrend(day_label="Sun", day_order=7, risk_value=91.0)
            ]
            db.add_all(trends)
            db.commit()
            logger.info("Seeded RiskTrends.")

        # 7. Action Recommendations
        if db.query(ActionRecommendation).count() == 0:
            recs = [
                ActionRecommendation(recommendation_text="Activate river-level monitoring in Goalpara and nearby embankments.", priority=1),
                ActionRecommendation(recommendation_text="Prepare evacuation teams for high-risk slope communities in Dima Hasao.", priority=2),
                ActionRecommendation(recommendation_text="Issue local SMS alerts to vulnerable settlements before peak rainfall hours.", priority=3),
                ActionRecommendation(recommendation_text="Deploy drainage inspection crews to flood-prone urban drainage channels.", priority=4)
            ]
            db.add_all(recs)
            db.commit()
            logger.info("Seeded ActionRecommendations.")

    except Exception as err:
        logger.error(f"Error seeding initial database data: {err}")
        db.rollback()
