export default function MapLegend() {
  return (
    <div className="map-legend">
      <div className="map-legend__title">AI Landslide Risk Levels</div>
      <div className="map-legend__item">
        <span className="map-legend__dot" style={{ backgroundColor: '#DC2626' }} />
        Critical Risk (75-100%)
      </div>
      <div className="map-legend__item">
        <span className="map-legend__dot" style={{ backgroundColor: '#EA580C' }} />
        High Risk (50-75%)
      </div>
      <div className="map-legend__item">
        <span className="map-legend__dot" style={{ backgroundColor: '#D97706' }} />
        Moderate Risk (25-50%)
      </div>
      <div className="map-legend__item">
        <span className="map-legend__dot" style={{ backgroundColor: '#16A34A' }} />
        Low Risk (0-25%)
      </div>
      <div className="map-legend__item">
        <span className="map-legend__dot" style={{ backgroundColor: '#0DAFAB' }} />
        Flood Plain Risk
      </div>
    </div>
  );
}
