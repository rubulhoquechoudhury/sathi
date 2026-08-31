import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, Tooltip } from 'react-leaflet';
import MapLegend from './MapLegend';
import { riskZones as fallbackRiskZones, MAP_CENTER, MAP_ZOOM } from '../data/riskZones';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

const RISK_LEVEL_COLORS = {
  CRITICAL: { fillColor: '#DC2626', fillOpacity: 0.45, color: '#991B1B', weight: 3 },
  HIGH: { fillColor: '#EA580C', fillOpacity: 0.40, color: '#C2410C', weight: 2.5 },
  MODERATE: { fillColor: '#D97706', fillOpacity: 0.35, color: '#B45309', weight: 2 },
  LOW: { fillColor: '#16A34A', fillOpacity: 0.30, color: '#15803D', weight: 2 },
  flood: { fillColor: '#0DAFAB', fillOpacity: 0.30, color: '#0F766E', weight: 2 },
  landslide: { fillColor: '#4B3AC2', fillOpacity: 0.35, color: '#3730A3', weight: 2 }
};

export default function MapView({ version = "default", height }) {
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function fetchLiveZones() {
      try {
        const response = await fetch('http://localhost:8000/api/v1/zones');
        if (response.ok) {
          const data = await response.json();
          if (isMounted && Array.isArray(data) && data.length > 0) {
            setZones(data);
            setLoading(false);
            return;
          }
        }
      } catch (err) {
        console.warn('Backend API offline, falling back to static risk zones:', err);
      }

      if (isMounted) {
        setZones(fallbackRiskZones);
        setLoading(false);
      }
    }

    fetchLiveZones();

    return () => {
      isMounted = false;
    };
  }, []);

  const getStyleForZone = (zone) => {
    if (zone.risk_level && RISK_LEVEL_COLORS[zone.risk_level]) {
      return RISK_LEVEL_COLORS[zone.risk_level];
    }
    if (zone.type && RISK_LEVEL_COLORS[zone.type]) {
      return RISK_LEVEL_COLORS[zone.type];
    }
    return RISK_LEVEL_COLORS.MODERATE;
  };

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
          const style = getStyleForZone(zone);
          const riskLevel = zone.risk_level || (zone.type === 'flood' ? 'Flood Risk' : 'Landslide Risk');
          const riskScore = zone.risk_score !== undefined ? zone.risk_score : 'N/A';
          const proba = zone.landslide_probability !== undefined ? (zone.landslide_probability * 100).toFixed(1) + '%' : 'N/A';

          return (
            <Polygon
              key={zone.id}
              positions={zone.coordinates}
              pathOptions={style}
            >
              <Tooltip direction="top" sticky>
                <div style={{ fontSize: '13px', lineHeight: '1.4' }}>
                  <strong style={{ fontSize: '14px', color: '#1E293B' }}>{zone.name}</strong>
                  <div style={{ marginTop: '4px', fontWeight: '600', color: style.color }}>
                    AI Risk Level: {riskLevel}
                  </div>
                  {zone.risk_score !== undefined && (
                    <div style={{ fontSize: '12px', color: '#475569' }}>
                      Risk Score: <strong>{riskScore}/100</strong> (Prob: {proba})
                    </div>
                  )}
                  {zone.sample_terrain && (
                    <div style={{ fontSize: '11px', color: '#64748B', marginTop: '2px' }}>
                      Slope: {zone.sample_terrain.slope}° | Elev: {zone.sample_terrain.elevation}m
                    </div>
                  )}
                </div>
              </Tooltip>
            </Polygon>
          );
        })}
      </MapContainer>

      <MapLegend />
    </div>
  );
}
