import { MapContainer, TileLayer, Polygon, Tooltip } from 'react-leaflet';
import MapLegend from './MapLegend';
import { riskZones, MAP_CENTER, MAP_ZOOM } from '../data/riskZones';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

const STYLES = {
  flood: {
    fillColor: '#0DAFAB',
    fillOpacity: 0.25,
    color: '#0DAFAB',
    weight: 2,
    opacity: 0.6,
  },
  landslide: {
    fillColor: '#4B3AC2',
    fillOpacity: 0.25,
    color: '#4B3AC2',
    weight: 2,
    opacity: 0.6,
  },
};

export default function MapView({version = "default" , height}) {
  return (
    <div className={`map-wrapper ${version}`}>
      <MapContainer
        center={MAP_CENTER}
        zoom={MAP_ZOOM}
        scrollWheelZoom={true}
        zoomControl={true}
        style={{ height:'100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {riskZones.map((zone) => (
          <Polygon
            key={zone.id}
            positions={zone.coordinates}
            pathOptions={STYLES[zone.type]}
          >
            <Tooltip direction="top" sticky>
              <strong>{zone.name}</strong>
              <br />
              {zone.type === 'flood' ? 'Flood Risk Zone' : 'Landslide Risk Zone'}
            </Tooltip>
          </Polygon>
        ))}
      </MapContainer>

      <MapLegend />
    </div>
  );
}
