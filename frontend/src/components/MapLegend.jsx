export default function MapLegend() {
  return (
    <div style={{
      position: 'absolute',
      bottom: '20px',
      right: '20px',
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(8px)',
      border: '1px solid #E2E8F0',
      borderRadius: '8px',
      padding: '12px 16px',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
      zIndex: 9999,
      fontSize: '12px',
      color: '#0F172A',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{
        fontSize: '11px',
        fontWeight: '700',
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        color: '#64748B',
        marginBottom: '8px'
      }}>
        AI Landslide & Flood Risk Levels
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', fontWeight: '600' }}>
        <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#DC2626', display: 'inline-block' }} />
        Critical Risk (75-100%)
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', fontWeight: '600' }}>
        <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#EA580C', display: 'inline-block' }} />
        High Risk (50-75%)
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', fontWeight: '600' }}>
        <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#EAB308', display: 'inline-block' }} />
        Moderate Risk (25-50%)
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', fontWeight: '600' }}>
        <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#16A34A', display: 'inline-block' }} />
        Low Risk (0-25%)
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '600' }}>
        <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#06B6D4', display: 'inline-block' }} />
        Flood Plain Risk
      </div>
    </div>
  );
}
