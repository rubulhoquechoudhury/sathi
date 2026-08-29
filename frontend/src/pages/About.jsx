import './Pages.css';

export default function About() {
  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">About Sathi</h1>
        <p className="page__subtitle">
          Sathi is a disaster-risk mapping platform that helps communities
          identify and prepare for probable flood and landslide hazards.
        </p>
      </div>

      <div className="page__section">
        <h2>Our Mission</h2>
        <p>
          We believe that access to clear, actionable risk information can save
          lives. Sathi visualizes probable disaster zones on an interactive map,
          making it easier for communities, planners, and responders to
          understand and act on environmental risks.
        </p>
      </div>

      <div className="page__section">
        <h2>How It Works</h2>
        <p>
          Sathi overlays flood and landslide risk areas onto OpenStreetMap data.
          Each risk zone is displayed as a transparent polygon, color-coded by
          hazard type — teal for flood-prone areas and purple for
          landslide-prone areas. Simply explore the map to see the risk
          landscape around you.
        </p>
      </div>

      <div className="page__section">
        <h2>Open & Accessible</h2>
        <p>
          Sathi is built with open-source tools and open data. Our goal is to
          keep disaster risk information free, accessible, and easy to
          understand for everyone.
        </p>
      </div>
    </div>
  );
}
