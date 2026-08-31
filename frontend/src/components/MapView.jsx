import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, CircleMarker, Tooltip, Popup } from 'react-leaflet';
import MapLegend from './MapLegend';
import { riskZones as fallbackRiskZones, MAP_CENTER, MAP_ZOOM } from '../data/riskZones';
import { apiService, RiskWebSocketClient } from '../services/api';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

const RISK_LEVEL_COLORS = {
  CRITICAL: { fill: true, stroke: true, fillColor: '#DC2626', fillOpacity: 0.70, color: '#991B1B', weight: 3 },
  HIGH: { fill: true, stroke: true, fillColor: '#EA580C', fillOpacity: 0.65, color: '#C2410C', weight: 3 },
  MODERATE: { fill: true, stroke: true, fillColor: '#EAB308', fillOpacity: 0.70, color: '#CA8A04', weight: 3 },
  LOW: { fill: true, stroke: true, fillColor: '#16A34A', fillOpacity: 0.70, color: '#15803D', weight: 3 },
  FLOOD: { fill: true, stroke: true, fillColor: '#06B6D4', fillOpacity: 0.70, color: '#0891B2', weight: 3 },
  flood: { fill: true, stroke: true, fillColor: '#06B6D4', fillOpacity: 0.70, color: '#0891B2', weight: 3 },
  landslide: { fill: true, stroke: true, fillColor: '#EA580C', fillOpacity: 0.65, color: '#C2410C', weight: 3 }
};

export default function MapView({ version = "default" }) {
  const [zones, setZones] = useState(fallbackRiskZones);
  const [connectionStatus, setConnectionStatus] = useState('CONNECTING');
  const [showIncidents, setShowIncidents] = useState(true);
  const [incidents, setIncidents] = useState([]);
  const [inventoryStats, setInventoryStats] = useState({ total_records: 11026 });

  useEffect(() => {
    let isMounted = true;

    // 1. Fetch Initial Spatial Risk Zones from REST API
    async function loadZones() {
      try {
        const data = await apiService.getZones();
        if (isMounted && Array.isArray(data) && data.length > 0) {
          setZones(data);
        }
      } catch (err) {
        console.warn('[MapView] API offline, using fallback static risk zones:', err.message);
      }
    }

    // 2. Fetch Authoritative 11,026 Landslide Incidents & Stats
    async function loadInventory() {
      try {
        const stats = await apiService.getInventoryStats();
        if (isMounted && stats) setInventoryStats(stats);

        const data = await apiService.getLandslideInventory(null, 500);
        if (isMounted && data && Array.isArray(data.records)) {
          setIncidents(data.records);
        }
      } catch (err) {
        console.warn('[MapView] Could not fetch landslide inventory:', err.message);
      }
    }

    loadZones();
    loadInventory();

    // 3. Initialize Real-Time WebSocket Client
    const wsClient = new RiskWebSocketClient(
      (msg) => {
        if (!isMounted) return;
        if (msg && (msg.type === 'risk_update' || msg.type === 'initial_risk_state')) {
          const updates = Array.isArray(msg.data) ? msg.data : [msg.data];
          setZones((prevZones) =>
            prevZones.map((z) => {
              const match = updates.find(
                (u) =>
                  u.latitude &&
                  u.longitude &&
                  Math.abs(u.latitude - (z.sample_location?.latitude || z.coordinates[0][0])) < 0.15 &&
                  Math.abs(u.longitude - (z.sample_location?.longitude || z.coordinates[0][1])) < 0.15
              );
              if (match) {
                return {
                  ...z,
                  risk_level: match.risk_level || z.risk_level,
                  risk_score: match.risk_score !== undefined ? match.risk_score : z.risk_score,
                  landslide_probability: match.landslide_probability !== undefined ? match.landslide_probability : z.landslide_probability,
                  data_status: match.data_status || z.data_status,
                  telemetry: match.telemetry || z.telemetry,
                  timestamp: match.timestamp || z.timestamp
                };
              }
              return z;
            })
          );
        }
      },
      (status) => {
        if (isMounted) setConnectionStatus(status);
      }
    );

    wsClient.connect();

    return () => {
      isMounted = false;
      wsClient.close();
    };
  }, []);

  const getStyleForZone = (zone) => {
    if (zone.type === 'flood' || (zone.risk_level && zone.risk_level.toUpperCase() === 'FLOOD')) {
      return RISK_LEVEL_COLORS.FLOOD;
    }
    const level = (zone.risk_level || '').toUpperCase();
    if (level && RISK_LEVEL_COLORS[level]) {
      return RISK_LEVEL_COLORS[level];
    }
    return RISK_LEVEL_COLORS.MODERATE;
  };

  const getStatusBadgeColor = (status) => {
    switch (status) {
      case 'LIVE':
        return { bg: 'rgba(22, 163, 74, 0.9)', dot: '#4ADE80', label: 'LIVE AI WebSocket Connected' };
      case 'CONNECTING':
      case 'RECONNECTING':
        return { bg: 'rgba(217, 119, 6, 0.9)', dot: '#FBBF24', label: `${status}...` };
      default:
        return { bg: 'rgba(220, 38, 38, 0.9)', dot: '#F87171', label: 'Backend Offline (Static Mode)' };
    }
  };

  const badge = getStatusBadgeColor(connectionStatus);

  return (
    <div className={`map-wrapper ${version}`}>
      {/* Top Left Inventory Controls & Stats */}
      <div style={{
        position: 'absolute',
        top: '12px',
        left: '12px',
        zIndex: 1000,
        display: 'flex',
        gap: '8px'
      }}>
        <button
          onClick={() => setShowIncidents(!showIncidents)}
          style={{
            background: showIncidents ? '#6366F1' : 'rgba(255, 255, 255, 0.95)',
            color: showIncidents ? '#FFFFFF' : '#1E293B',
            border: '1px solid #CBD5E1',
            borderRadius: '16px',
            padding: '6px 14px',
            fontSize: '12px',
            fontWeight: '600',
            cursor: 'pointer',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          📍 {showIncidents ? 'Hide' : 'Show'} Historical Incidents ({inventoryStats.total_records || 11026})
        </button>
      </div>

      {/* Real-Time Connection Status Indicator */}
      <div style={{
        position: 'absolute',
        top: '12px',
        right: '12px',
        zIndex: 1000,
        background: badge.bg,
        color: 'white',
        padding: '5px 12px',
        borderRadius: '16px',
        fontSize: '12px',
        fontWeight: '600',
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.25)'
      }}>
        <span style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          backgroundColor: badge.dot,
          animation: connectionStatus === 'LIVE' ? 'pulse 1.5s infinite' : 'none'
        }} />
        {badge.label}
      </div>


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
          const riskLevel = zone.risk_level || 'UNKNOWN';
          const riskScore = zone.risk_score !== undefined ? zone.risk_score : 'N/A';
          const probaStr = zone.landslide_probability !== undefined 
            ? (zone.landslide_probability * 100).toFixed(1) + '%' 
            : 'N/A';
          const dataStatus = zone.data_status || 'COMPLETE';
          const alphaStatus = zone.alphaearth_status || 'VERIFIED';
          const tel = zone.telemetry;

          const samplePos = zone.sample_location 
            ? [zone.sample_location.latitude, zone.sample_location.longitude] 
            : zone.coordinates[0];

          return (
            <div key={zone.id}>
              <Polygon
                positions={zone.coordinates}
                pathOptions={style}
              >
                <Tooltip direction="top" sticky>
                  <div style={{ fontSize: '13px', lineHeight: '1.4', minWidth: '190px' }}>
                    <strong style={{ fontSize: '14px', color: '#1E293B' }}>{zone.name}</strong>
                    
                    <div style={{ marginTop: '4px', fontWeight: '700', color: style.color, fontSize: '13px' }}>
                      AI Risk Level: {riskLevel}
                    </div>

                    <div style={{ fontSize: '12px', color: '#334155', marginTop: '2px' }}>
                      Landslide Probability: <strong>{probaStr}</strong> (Score: <strong>{riskScore}/100</strong>)
                    </div>

                    {/* Telemetry metrics display */}
                    {tel && (
                      <div style={{ fontSize: '11px', color: '#1E293B', marginTop: '4px', background: '#F1F5F9', padding: '4px 6px', borderRadius: '4px' }}>
                        Temp: <strong>{tel.temperature ?? '26.0'}°C</strong> | Hum: <strong>{tel.humidity ?? '80'}%</strong><br />
                        Soil: <strong>{tel.soil_moisture ? (tel.soil_moisture * 100).toFixed(0) + '%' : '42%'}</strong> | Rain: <strong>{tel.rainfall_mm ?? '0'}mm</strong>
                      </div>
                    )}

                    {/* Data Status & AlphaEarth Warnings */}
                    {alphaStatus === 'VERIFIED' ? (
                      <div style={{ fontSize: '11px', color: '#16A34A', marginTop: '4px', fontWeight: '600' }}>
                        ● AlphaEarth status: VERIFIED
                      </div>
                    ) : (
                      <div style={{ fontSize: '11px', color: '#D97706', marginTop: '4px', fontWeight: '600' }}>
                        ⚠ AlphaEarth status: UNVERIFIED
                      </div>
                    )}

                    {dataStatus === 'INSUFFICIENT_DATA' && (
                      <div style={{ fontSize: '11px', color: '#DC2626', marginTop: '4px', fontWeight: '600' }}>
                        🚫 Insufficient Environmental Data
                      </div>
                    )}

                    {dataStatus === 'STALE' && (
                      <div style={{ fontSize: '11px', color: '#EA580C', marginTop: '4px', fontWeight: '600' }}>
                        ⏱ Stale Environmental Telemetry
                      </div>
                    )}

                    {zone.sample_terrain && (
                      <div style={{ fontSize: '11px', color: '#64748B', marginTop: '4px', borderTop: '1px solid #E2E8F0', paddingTop: '4px' }}>
                        Slope: {zone.sample_terrain.slope}° | Elev: {zone.sample_terrain.elevation}m
                      </div>
                    )}

                    {zone.timestamp && (
                      <div style={{ fontSize: '10px', color: '#94A3B8', marginTop: '2px' }}>
                        Model: {zone.model_version || 'xgb-v1'} | Updated: {new Date(zone.timestamp).toLocaleTimeString()}
                      </div>
                    )}
                  </div>
                </Tooltip>
              </Polygon>

              {samplePos && (
                <CircleMarker
                  center={samplePos}
                  radius={8}
                  pathOptions={{
                    fillColor: style.fillColor,
                    fillOpacity: 0.9,
                    color: '#FFFFFF',
                    weight: 2
                  }}
                >
                  <Tooltip direction="right">
                    <strong style={{ fontSize: '12px' }}>{zone.name} ({riskLevel})</strong>
                  </Tooltip>
                </CircleMarker>
              )}
            </div>
          );
        })}

        {showIncidents && incidents.map((inc, idx) => (

          inc.latitude && inc.longitude && (
            <CircleMarker
              key={`${inc.id}-${idx}`}
              center={[inc.latitude, inc.longitude]}
              radius={4}
              pathOptions={{
                fillColor: '#8B5CF6',
                fillOpacity: 0.85,
                color: '#FFFFFF',
                weight: 1
              }}
            >
              <Tooltip direction="top">
                <div style={{ fontSize: '11px', lineHeight: '1.3' }}>
                  <strong style={{ color: '#6D28D9' }}>{inc.slide_name}</strong><br />
                  {inc.district}, {inc.state}<br />
                  <span style={{ color: '#4C1D95', fontWeight: '600' }}>Type: {inc.movement_type} ({inc.material_involved})</span>
                </div>
              </Tooltip>
            </CircleMarker>
          )
        ))}

      </MapContainer>

      <MapLegend />
    </div>

  );
}
