/**
 * Sample disaster risk zone data.
 * Polygons are positioned around Assam / Northeast India for realism.
 * Each zone has: id, name, type ('flood' | 'landslide'), coordinates, and telemetry.
 */

export const MAP_CENTER = [26.15, 91.75];
export const MAP_ZOOM = 10;

export const riskZones = [
  // — Flood Risk Zones —
  {
    id: 'flood-1',
    name: 'Brahmaputra Floodplain – West',
    type: 'flood',
    risk_level: 'HIGH',
    landslide_probability: 0.68,
    coordinates: [
      [26.22, 91.55],
      [26.28, 91.62],
      [26.25, 91.72],
      [26.18, 91.70],
      [26.15, 91.60],
    ],
    telemetry: {
      temperature: 28.2,
      humidity: 86,
      soil_moisture: 0.52,
      rainfall_mm: 32.5
    }
  },
  {
    id: 'flood-2',
    name: 'Brahmaputra Floodplain – East',
    type: 'flood',
    risk_level: 'MODERATE',
    landslide_probability: 0.45,
    coordinates: [
      [26.12, 91.78],
      [26.18, 91.85],
      [26.20, 91.95],
      [26.14, 91.98],
      [26.08, 91.88],
    ],
    telemetry: {
      temperature: 27.5,
      humidity: 80,
      soil_moisture: 0.41,
      rainfall_mm: 18.0
    }
  },
  {
    id: 'flood-3',
    name: 'Kolong River Basin',
    type: 'flood',
    risk_level: 'LOW',
    landslide_probability: 0.18,
    coordinates: [
      [26.05, 91.60],
      [26.10, 91.68],
      [26.08, 91.76],
      [26.02, 91.73],
      [26.00, 91.64],
    ],
    telemetry: {
      temperature: 26.8,
      humidity: 74,
      soil_moisture: 0.32,
      rainfall_mm: 5.2
    }
  },

  // — Landslide Risk Zones —
  {
    id: 'landslide-1',
    name: 'Meghalaya Foothills – North',
    type: 'landslide',
    risk_level: 'CRITICAL',
    landslide_probability: 0.92,
    coordinates: [
      [25.98, 91.82],
      [26.02, 91.90],
      [25.99, 91.96],
      [25.93, 91.92],
      [25.94, 91.84],
    ],
    telemetry: {
      temperature: 24.5,
      humidity: 92,
      soil_moisture: 0.65,
      rainfall_mm: 54.0
    }
  },
  {
    id: 'landslide-2',
    name: 'Ri-Bhoi Hill Slopes',
    type: 'landslide',
    risk_level: 'HIGH',
    landslide_probability: 0.76,
    coordinates: [
      [25.90, 91.65],
      [25.95, 91.72],
      [25.93, 91.80],
      [25.87, 91.78],
      [25.86, 91.69],
    ],
    telemetry: {
      temperature: 25.0,
      humidity: 88,
      soil_moisture: 0.58,
      rainfall_mm: 41.2
    }
  },
];
