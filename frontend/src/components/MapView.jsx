import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, Tooltip } from 'react-leaflet';
import MapLegend from './MapLegend';
import { riskZones as staticRiskZones, MAP_CENTER, MAP_ZOOM } from '../data/riskZones';
import { apiService } from '../services/api';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

const STYLES = {
  flood: {
    fillColor: '#EAB308',
    fillOpacity: 0.35,
    color: '#CA8A04',
    weight: 2,
    opacity: 0.8,
  },
  landslide: {
    fillColor: '#EF4444',
    fillOpacity: 0.35,
    color: '#DC2626',
    weight: 2,
    opacity: 0.8,
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
          // Set first zone as initial default selected if available
          if (!selectedZone) setSelectedZone(data[0]);
        }
      } catch (err) {
        console.warn('[MapView] Using static risk zones fallback:', err.message);
        if (!selectedZone) setSelectedZone(staticRiskZones[0]);
      }
    }
    fetchLiveZones();
  }, []);

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
          const tel = getTelemetry(zone);
          const isSelected = selectedZone?.id === zone.id;

          return (
            <Polygon
              key={zone.id}
              positions={zone.coordinates}
              pathOptions={{
                ...(STYLES[zone.type] || STYLES.landslide),
                weight: isSelected ? 4 : 2,
                fillOpacity: isSelected ? 0.55 : 0.35
              }}
              eventHandlers={{
                click: () => setSelectedZone(zone)
              }}
            >
              <Tooltip direction="top" sticky>
                <div style={{ fontSize: '12px', lineHeight: '1.4' }}>
                  <strong style={{ fontSize: '13px', color: '#0F172A' }}>{zone.name}</strong>
                  <br />
                  <span style={{
                    fontWeight: '700',
                    color: zone.type === 'flood' ? '#CA8A04' : '#DC2626'
                  }}>
                    {zone.type === 'flood' ? 'Flood Risk Zone' : 'Landslide Risk Zone'}
                  </span>
                  {zone.risk_level && (
                    <span style={{ marginLeft: '6px', fontSize: '11px', background: '#F1F5F9', padding: '1px 5px', borderRadius: '4px' }}>
                      {zone.risk_level}
                    </span>
                  )}
                  <hr style={{ margin: '4px 0', border: 'none', borderTop: '1px solid #E2E8F0' }} />
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
              <span style={{
                fontSize: '11px',
                fontWeight: '700',
                color: selectedZone.type === 'flood' ? '#CA8A04' : '#DC2626'
              }}>
                {selectedZone.type === 'flood' ? 'Flood Risk Zone' : 'Landslide Risk Zone'}
                {selectedZone.risk_level ? ` • ${selectedZone.risk_level}` : ''}
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
