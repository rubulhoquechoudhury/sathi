/**
 * Sample disaster risk zone data.
 * Polygons are positioned around Assam / Northeast India for realism.
 * Each zone has: id, name, type ('flood' | 'landslide'), and coordinates.
 */

export const MAP_CENTER = [26.15, 91.75];
export const MAP_ZOOM = 10;

export const riskZones = [
  // — Flood Risk Zones —
  {
    id: 'flood-1',
    name: 'Brahmaputra Floodplain – West',
    type: 'flood',
    coordinates: [
      [26.22, 91.55],
      [26.28, 91.62],
      [26.25, 91.72],
      [26.18, 91.70],
      [26.15, 91.60],
    ],
  },
  {
    id: 'flood-2',
    name: 'Brahmaputra Floodplain – East',
    type: 'flood',
    coordinates: [
      [26.12, 91.78],
      [26.18, 91.85],
      [26.20, 91.95],
      [26.14, 91.98],
      [26.08, 91.88],
    ],
  },
  {
    id: 'flood-3',
    name: 'Kolong River Basin',
    type: 'flood',
    coordinates: [
      [26.05, 91.60],
      [26.10, 91.68],
      [26.08, 91.76],
      [26.02, 91.73],
      [26.00, 91.64],
    ],
  },

  // — Landslide Risk Zones —
  {
    id: 'landslide-1',
    name: 'Meghalaya Foothills – North',
    type: 'landslide',
    coordinates: [
      [25.98, 91.82],
      [26.02, 91.90],
      [25.99, 91.96],
      [25.93, 91.92],
      [25.94, 91.84],
    ],
  },
  {
    id: 'landslide-2',
    name: 'Ri-Bhoi Hill Slopes',
    type: 'landslide',
    coordinates: [
      [25.90, 91.65],
      [25.95, 91.72],
      [25.93, 91.80],
      [25.87, 91.78],
      [25.86, 91.69],
    ],
  },
];
