import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, Tooltip } from 'react-leaflet';
import MapLegend from './MapLegend';
import { riskZones as staticRiskZones, MAP_CENTER, MAP_ZOOM } from '../data/riskZones';
import { apiService } from '../services/api';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

// 4-Tier Risk Category Styles & Alert Badges
const CATEGORY_STYLES = {
  CRITICAL: {
    fillColor: '#EF4444',
    fillOpacity: 0.40,
    color: '#DC2626',
    weight: 2,
    opacity: 0.90,
    label: 'Critical Risk',
    badgeBg: '#FEE2E2',
    badgeColor: '#991B1B',
    alertText: '🚨 ALERT: CRITICAL DANGER'
  },
  HIGH: {
    fillColor: '#F97316',
    fillOpacity: 0.40,
    color: '#EA580C',
    weight: 2,
    opacity: 0.90,
    label: 'High Risk',
    badgeBg: '#FFEDD5',
    badgeColor: '#C2410C',
    alertText: '⚠️ ALERT: HIGH WARNING'
  },
  FLOOD_PLAIN: {
    fillColor: '#3B82F6',
    fillOpacity: 0.40,
    color: '#1D4ED8',
    weight: 2,
    opacity: 0.90,
    label: 'Flood Plain Risk',
    badgeBg: '#DBEAFE',
    badgeColor: '#1E40AF',
    alertText: '⚠️ ALERT: FLOOD WATCH'
  },

  LOW: {
    fillColor: '#22C55E',
    fillOpacity: 0.40,
    color: '#16A34A',
    weight: 2,
    opacity: 0.90,
    label: 'Low Risk',
    badgeBg: '#DCFCE7',
    badgeColor: '#166534',
    alertText: '🛡️ ALERT: NORMAL MONITORING'
  },
};

export default function MapView({ version = "default", height }) {
  const [zones, setZones] = useState(staticRiskZones);
  const [selectedZone, setSelectedZone] = useState(null);

  useEffect(() => {
    async function fetchLiveZones() {
      try {
        const data = await apiService.getZones();
        if (Array.isArray(data) && data.length > 0) {
          setZones(data);
          if (!selectedZone) setSelectedZone(data[0]);
        }
      } catch (err) {
        console.warn('[MapView] Using static risk zones fallback:', err.message);
        if (!selectedZone) setSelectedZone(staticRiskZones[0]);
      }
    }
    fetchLiveZones();
  }, []);

  const getRiskCategory = (zone) => {
    if (!zone) return 'LOW';
    const cat = (zone.risk_category || zone.risk_level || '').toUpperCase().replace(/\s+/g, '_');

    if (cat.includes('CRITICAL')) return 'CRITICAL';
    if (cat.includes('HIGH')) return 'HIGH';
    if (cat.includes('FLOOD') || cat.includes('PLAIN') || zone.type === 'flood') return 'FLOOD_PLAIN';
    if (cat.includes('LOW')) return 'LOW';

    const prob = zone.landslide_probability || 0.0;
    if (prob >= 0.80) return 'CRITICAL';
    if (prob >= 0.50) return 'HIGH';
    if (prob >= 0.25) return 'FLOOD_PLAIN';
    return 'LOW';
  };

  const getProneLabel = (zone) => {
    if (!zone) return 'Landslide Prone Area';
    return zone.type === 'flood' ? '🌊 Flood Prone Area' : '⛰️ Landslide Prone Area';
  };

  const formatSoilMoisture = (val) => {
    if (val === null || val === undefined) return '42%';
    if (typeof val === 'number') {
      return val > 1 ? `${Math.round(val)}%` : `${Math.round(val * 100)}%`;
    }
    return val;
  };

  const getTelemetry = (zone) => {
    const tel = zone?.telemetry || {};
    return {
      temp: tel.temperature !== undefined && tel.temperature !== null ? `${tel.temperature}°C` : '26.5°C',
      humidity: tel.humidity !== undefined && tel.humidity !== null ? `${tel.humidity}%` : '82%',
      soil: formatSoilMoisture(tel.soil_moisture),
      rainfall: tel.rainfall_mm !== undefined && tel.rainfall_mm !== null ? `${tel.rainfall_mm} mm` : '15.0 mm'
    };
  };

  const selectedCategory = getRiskCategory(selectedZone);
  const selectedStyle = CATEGORY_STYLES[selectedCategory] || CATEGORY_STYLES.LOW;
  const activeTelemetry = getTelemetry(selectedZone);

  return (
    <div className={`map-wrapper ${version}`}>
      <MapContainer
        center={MAP_CENTER}
        zoom={MAP_ZOOM}
        scrollWheelZoom={true}
        zoomControl={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {zones.map((zone) => {
          const catKey = getRiskCategory(zone);
          const styleConfig = CATEGORY_STYLES[catKey] || CATEGORY_STYLES.LOW;
          const proneLabel = getProneLabel(zone);
          const tel = getTelemetry(zone);
          const isSelected = selectedZone?.id === zone.id;

          return (
            <Polygon
              key={zone.id}
              positions={zone.coordinates}
              pathOptions={{
                ...styleConfig,
                weight: isSelected ? 4 : 2,
                fillOpacity: isSelected ? 0.65 : 0.40
              }}
              eventHandlers={{
                click: () => setSelectedZone(zone)
              }}
            >
              <Tooltip direction="top" sticky>
                <div style={{ fontSize: '12px', lineHeight: '1.4', padding: '2px' }}>
                  <strong style={{ fontSize: '13px', color: '#0F172A', display: 'block', marginBottom: '2px' }}>
                    {zone.name}
                  </strong>

                  {/* Prone Designation */}
                  <div style={{
                    fontWeight: '700',
                    fontSize: '12px',
                    color: zone.type === 'flood' ? '#2563EB' : '#DC2626',

                    marginBottom: '4px'
                  }}>
                    {proneLabel}
                  </div>

                  {/* Alert Status Badge */}
                  <div style={{
                    display: 'inline-block',
                    background: styleConfig.badgeBg,
                    color: styleConfig.badgeColor,
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontSize: '11px',
                    fontWeight: '800',
                    marginBottom: '6px'
                  }}>
                    {styleConfig.alertText}
                  </div>

                  <hr style={{ margin: '4px 0', border: 'none', borderTop: '1px solid #E2E8F0' }} />

                  {/* Environmental Telemetry */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 8px', fontSize: '11px' }}>
                    <span>🌡️ Temp: <strong>{tel.temp}</strong></span>
                    <span>💧 Hum: <strong>{tel.humidity}</strong></span>
                    <span>🌱 Soil: <strong>{tel.soil}</strong></span>
                    <span>🌧️ Rain: <strong>{tel.rainfall}</strong></span>
                  </div>
                </div>
              </Tooltip>
            </Polygon>
          );
        })}
      </MapContainer>

      {/* Selected Zone Telemetry Overlay Panel */}
      {selectedZone && (
        <div className="zone-telemetry-panel">
          <div className="zone-telemetry-panel__header">
            <div>
              <div className="zone-telemetry-panel__title">{selectedZone.name}</div>
              <div style={{ fontSize: '12px', fontWeight: '700', color: selectedZone.type === 'flood' ? '#2563EB' : '#DC2626', marginTop: '2px' }}>

                {getProneLabel(selectedZone)}
              </div>
              <span style={{
                fontSize: '11px',
                fontWeight: '800',
                color: selectedStyle.badgeColor,
                background: selectedStyle.badgeBg,
                padding: '2px 8px',
                borderRadius: '4px',
                display: 'inline-block',
                marginTop: '4px'
              }}>
                {selectedStyle.alertText}
              </span>
            </div>
            <button
              className="zone-telemetry-panel__close"
              onClick={() => setSelectedZone(null)}
              title="Close panel"
            >
              ×
            </button>
          </div>

          <div className="telemetry-grid">
            <div className="telemetry-item">
              <div className="telemetry-item__label">🌡️ Temperature</div>
              <div className="telemetry-item__val">{activeTelemetry.temp}</div>
            </div>
            <div className="telemetry-item">
              <div className="telemetry-item__label">💧 Humidity</div>
              <div className="telemetry-item__val">{activeTelemetry.humidity}</div>
            </div>
            <div className="telemetry-item">
              <div className="telemetry-item__label">🌱 Soil Moisture</div>
              <div className="telemetry-item__val">{activeTelemetry.soil}</div>
            </div>
            <div className="telemetry-item">
              <div className="telemetry-item__label">🌧️ 1h Rainfall</div>
              <div className="telemetry-item__val">{activeTelemetry.rainfall}</div>
            </div>
          </div>
        </div>
      )}

      <MapLegend />
    </div>
  );
}
