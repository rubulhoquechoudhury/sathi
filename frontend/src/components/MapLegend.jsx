export default function MapLegend() {
  return (
    <div className="map-legend">
      <div className="map-legend__title">Risk Layers</div>
      <div className="map-legend__item">
        <span className="map-legend__dot map-legend__dot--flood" />
        Flood Risk
      </div>
      <div className="map-legend__item">
        <span className="map-legend__dot map-legend__dot--landslide" />
        Landslide Risk
      </div>
    </div>
  );
}
