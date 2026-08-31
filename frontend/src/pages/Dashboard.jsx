import './dashboard.css';

const statCards = [
  { label: 'Flood alerts', value: '12', delta: '+3 since yesterday', tone: 'flood' },
  { label: 'Landslide watch', value: '08', delta: '+2 high-priority zones', tone: 'landslide' },
  { label: 'People at risk', value: '2.4K', delta: 'Across 6 districts', tone: 'risk' },
  { label: 'Rainfall forecast', value: '62 mm', delta: '24h cumulative', tone: 'rain' },
];

const zoneSummary = [
  { district: 'Kamrup', flood: 78, landslide: 42, status: 'Moderate' },
  { district: 'Goalpara', flood: 88, landslide: 55, status: 'High' },
  { district: 'Dima Hasao', flood: 46, landslide: 83, status: 'Critical' },
  { district: 'Karbi Anglong', flood: 62, landslide: 71, status: 'High' },
  { district: 'West Khasi Hills', flood: 39, landslide: 90, status: 'Critical' },
];

const alerts = [
  { type: 'Flood', title: 'Brahmaputra basin surge', time: '10 mins ago', severity: 'High', description: 'River level above seasonal average near Kamrup and Goalpara.' },
  { type: 'Landslide', title: 'Slope instability alert', time: '28 mins ago', severity: 'Critical', description: 'Heavy rain and loose soil detected in Dima Hasao foothills.' },
  { type: 'Rainfall', title: 'Monsoon intensity watch', time: '1 hr ago', severity: 'Moderate', description: 'Persistent rainfall is increasing runoff in the eastern hill belts.' },
];

const recommendations = [
  'Activate river-level monitoring in Goalpara and nearby embankments.',
  'Prepare evacuation teams for high-risk slope communities in Dima Hasao.',
  'Issue local SMS alerts to vulnerable settlements before peak rainfall hours.',
  'Deploy drainage inspection crews to flood-prone urban drainage channels.',
];

const trendData = [
  { label: 'Mon', value: 42 },
  { label: 'Tue', value: 56 },
  { label: 'Wed', value: 60 },
  { label: 'Thu', value: 74 },
  { label: 'Fri', value: 68 },
  { label: 'Sat', value: 86 },
  { label: 'Sun', value: 91 },
];

export default function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <span className="section-kicker">Operations overview</span>
          <h1>Flood & landslide risk dashboard</h1>
        </div>
        <button type="button" className="dashboard-action">Export report</button>
      </div>

      <section className="stats-grid">
        {statCards.map((card) => (
          <article key={card.label} className={`stat-card stat-card--${card.tone}`}>
            <div className="stat-card__label-row">
              <span className="stat-card__label">{card.label}</span>
              <span className="stat-card__dot" />
            </div>
            <div className="stat-card__value">{card.value}</div>
            <div className="stat-card__delta">{card.delta}</div>
          </article>
        ))}
      </section>

      <section className="dashboard-grid">
        <article className="panel risk-panel">
          <div className="panel__header">
            <h2>Regional risk summary</h2>
            <span className="panel__tag">Live</span>
          </div>

          <div className="risk-table">
            <div className="risk-table__head">
              <span>District</span>
              <span>Flood</span>
              <span>Landslide</span>
              <span>Status</span>
            </div>

            {zoneSummary.map((zone) => (
              <div key={zone.district} className="risk-table__row">
                <span>{zone.district}</span>
                <span>
                  <div className="mini-bar">
                    <span style={{ width: `${zone.flood}%` }} className="mini-bar__fill mini-bar__fill--flood" />
                  </div>
                </span>
                <span>
                  <div className="mini-bar">
                    <span style={{ width: `${zone.landslide}%` }} className="mini-bar__fill mini-bar__fill--landslide" />
                  </div>
                </span>
                <span className={`risk-pill risk-pill--${zone.status.toLowerCase()}`}>{zone.status}</span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel alert-panel">
          <div className="panel__header">
            <h2>Current alerts</h2>
            <span className="panel__tag panel__tag--alert">3 active</span>
          </div>

          <div className="alert-list">
            {alerts.map((alert) => (
              <div key={`${alert.type}-${alert.title}`} className="alert-item">
                <div className="alert-item__topline">
                  <span className="alert-pill alert-pill--flood">{alert.type}</span>
                  <span className="alert-time">{alert.time}</span>
                </div>
                <h3>{alert.title}</h3>
                <p>{alert.description}</p>
                <div className="alert-item__footer">
                  <span className={`severity severity--${alert.severity.toLowerCase()}`}>{alert.severity}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="bottom-grid">
        <article className="panel trend-panel">
          <div className="panel__header">
            <h2>7-day risk trend</h2>
            <span className="panel__tag">Forecast</span>
          </div>

          <div className="trend-chart">
            {trendData.map((point) => (
              <div key={point.label} className="trend-column">
                <div className="trend-column__value" style={{ height: `${point.value}%` }} />
                <span>{point.label}</span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel action-panel">
          <div className="panel__header">
            <h2>Recommended action</h2>
          </div>

          <ul className="recommendation-list">
            {recommendations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </section>
    </div>
  );
}
