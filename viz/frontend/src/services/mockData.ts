import { ActiveTyphoonItem, StormTrackResponse, ForecastResponse, Fix } from '../types';

// Helper to generate a polygon ring around a center lat/lon with given radius in km
function generateCircleRing(lat: number, lon: number, radiusKm: number): number[][] {
  const ring: number[][] = [];
  const earthRadiusKm = 6371.0;
  for (let angle = 0; angle <= 360; angle += 15) {
    const rad = (angle * Math.PI) / 180.0;
    const dLat = (radiusKm / earthRadiusKm) * (180.0 / Math.PI);
    const dLon = ((radiusKm / earthRadiusKm) * (180.0 / Math.PI)) / Math.cos((lat * Math.PI) / 180.0);
    const pLat = lat + dLat * Math.cos(rad);
    const pLon = lon + dLon * Math.sin(rad);
    ring.push([Number(pLon.toFixed(4)), Number(pLat.toFixed(4))]);
  }
  return ring;
}

// 1. Super Typhoon YAGI (2024) - Bão Số 3
export const MOCK_STORM_YAGI: ActiveTyphoonItem = {
  id: 'WP112024',
  name: 'YAGI',
  name_vi: 'Bão số 3 (Yagi)',
  year: 2024,
  observation_count: 14,
  status: 'active',
  latest: {
    timestamp: '2024-09-07T06:00:00Z',
    lat: 20.6,
    lon: 107.2,
    wind_ms: 55.0, // ~198 km/h, Cấp 16
    pressure_hpa: 935.0,
    intensity: 'SUPERTY',
    source: 'NCHMF / JMA',
    wind_kmh: 198,
    wind_knot: 107,
    beaufort_level: 16,
    bearing_deg: 290,
    speed_kmh: 22,
  },
};

export const MOCK_TRACK_YAGI: StormTrackResponse = {
  storm_id: 'WP112024',
  observations: [
    {
      timestamp: '2024-09-03T18:00:00Z',
      lat: 17.5,
      lon: 119.8,
      wind_ms: 23.0,
      pressure_hpa: 994.0,
      intensity: 'TS',
      source: 'JMA',
      wind_kmh: 83,
      beaufort_level: 9,
    },
    {
      timestamp: '2024-09-04T06:00:00Z',
      lat: 18.2,
      lon: 118.1,
      wind_ms: 30.0,
      pressure_hpa: 982.0,
      intensity: 'STS',
      source: 'JMA',
      wind_kmh: 108,
      beaufort_level: 11,
    },
    {
      timestamp: '2024-09-04T18:00:00Z',
      lat: 18.8,
      lon: 116.0,
      wind_ms: 40.0,
      pressure_hpa: 965.0,
      intensity: 'TY',
      source: 'JMA',
      wind_kmh: 144,
      beaufort_level: 13,
    },
    {
      timestamp: '2024-09-05T06:00:00Z',
      lat: 19.2,
      lon: 114.5,
      wind_ms: 52.0,
      pressure_hpa: 940.0,
      intensity: 'STY',
      source: 'JMA',
      wind_kmh: 187,
      beaufort_level: 16,
    },
    {
      timestamp: '2024-09-05T18:00:00Z',
      lat: 19.6,
      lon: 112.4,
      wind_ms: 58.0,
      pressure_hpa: 920.0,
      intensity: 'SUPERTY',
      source: 'JMA',
      wind_kmh: 209,
      beaufort_level: 17,
    },
    {
      timestamp: '2024-09-06T06:00:00Z',
      lat: 19.9,
      lon: 110.8,
      wind_ms: 60.0,
      pressure_hpa: 915.0,
      intensity: 'SUPERTY',
      source: 'JMA',
      wind_kmh: 216,
      beaufort_level: 17,
    },
    {
      timestamp: '2024-09-06T18:00:00Z',
      lat: 20.2,
      lon: 108.9,
      wind_ms: 55.0,
      pressure_hpa: 930.0,
      intensity: 'SUPERTY',
      source: 'NCHMF / JMA',
      wind_kmh: 198,
      beaufort_level: 16,
    },
    {
      timestamp: '2024-09-07T00:00:00Z',
      lat: 20.4,
      lon: 108.0,
      wind_ms: 55.0,
      pressure_hpa: 935.0,
      intensity: 'SUPERTY',
      source: 'NCHMF / JMA',
      wind_kmh: 198,
      beaufort_level: 16,
    },
    {
      timestamp: '2024-09-07T06:00:00Z',
      lat: 20.6,
      lon: 107.2, // Near Bach Long Vi island & approaching Quang Ninh - Hai Phong
      wind_ms: 52.0,
      pressure_hpa: 940.0,
      intensity: 'SUPERTY',
      source: 'NCHMF / JMA',
      wind_kmh: 187,
      beaufort_level: 16,
    },
  ],
  forecast: {
    forecast_id: 'fc-yagi-001',
    storm_id: 'WP112024',
    issue_time: '2024-09-07T06:00:00Z',
    generated_at: '2024-09-07T06:05:00Z',
    model_version: 'LSTM-Attention-v1.4.2 (Staging Candidate)',
    model_kind: 'trained-model',
    dataset_version: 'best-track-v2024.1',
    sources: ['NCHMF', 'JMA', 'JTWC'],
    uncertainty_method: '80th percentile validation radial error; empirical calibration',
    warnings: [
      'Cực kỳ nguy hiểm: Bão tiến sát bờ biển Quảng Ninh - Hải Phòng với sức gió trên cấp 14-15.',
      'Sóng biển cao 5-7m tại Vịnh Bắc Bộ, nước dâng do bão 1.5-2.0m.',
    ],
    disclaimer: 'Hệ thống hỗ trợ ra quyết định thử nghiệm; không thay thế bản tin NCHMF.',
    points: [
      {
        horizon_hours: 6,
        valid_time: '2024-09-07T12:00:00Z',
        lat: 20.9,
        lon: 106.8, // Landfall Quang Ninh - Hai Phong
        intensity: 'SUPERTY',
        radius_km: 35.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(20.9, 106.8, 35.0)],
        },
        wind_ms: 45.0,
        pressure_hpa: 955.0,
      },
      {
        horizon_hours: 12,
        valid_time: '2024-09-07T18:00:00Z',
        lat: 21.1,
        lon: 105.8, // Passing directly over Hanoi / Hai Duong
        intensity: 'TY',
        radius_km: 55.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(21.1, 105.8, 55.0)],
        },
        wind_ms: 35.0,
        pressure_hpa: 975.0,
      },
      {
        horizon_hours: 24,
        valid_time: '2024-09-08T06:00:00Z',
        lat: 21.4,
        lon: 104.2, // Yen Bai - Phu Tho mountainous region
        intensity: 'STS',
        radius_km: 90.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(21.4, 104.2, 90.0)],
        },
        wind_ms: 26.0,
        pressure_hpa: 990.0,
      },
      {
        horizon_hours: 48,
        valid_time: '2024-09-09T06:00:00Z',
        lat: 21.8,
        lon: 101.5, // Northern Laos / Upper Northwest
        intensity: 'TD',
        radius_km: 150.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(21.8, 101.5, 150.0)],
        },
        wind_ms: 15.0,
        pressure_hpa: 1004.0,
      },
      {
        horizon_hours: 72,
        valid_time: '2024-09-10T06:00:00Z',
        lat: 22.1,
        lon: 99.0, // Dissipated low pressure zone
        intensity: 'UNK',
        radius_km: 220.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(22.1, 99.0, 220.0)],
        },
        wind_ms: 11.0,
        pressure_hpa: 1008.0,
      },
    ],
  },
};

// 2. Active East Sea Simulation: Typhoon TRAMI (Bão mô phỏng Biển Đông)
export const MOCK_STORM_SIM: ActiveTyphoonItem = {
  id: 'WP202601',
  name: 'TRAMI',
  name_vi: 'Bão số 6 (Trà Mi - Mô Phỏng)',
  year: 2026,
  observation_count: 8,
  status: 'active',
  latest: {
    timestamp: new Date().toISOString(),
    lat: 16.2,
    lon: 113.8, // East of Hoang Sa (Paracel Islands)
    wind_ms: 38.0, // ~137 km/h, Cấp 12-13
    pressure_hpa: 970.0,
    intensity: 'TY',
    source: 'NCHMF Radar / Live Simulation',
    wind_kmh: 137,
    wind_knot: 74,
    beaufort_level: 13,
    bearing_deg: 280,
    speed_kmh: 20,
  },
};

export const MOCK_TRACK_SIM: StormTrackResponse = {
  storm_id: 'WP202601',
  observations: [
    {
      timestamp: new Date(Date.now() - 36 * 3600 * 1000).toISOString(),
      lat: 15.1,
      lon: 120.5,
      wind_ms: 20.0,
      pressure_hpa: 998.0,
      intensity: 'TS',
      source: 'PAGASA',
      wind_kmh: 72,
      beaufort_level: 8,
    },
    {
      timestamp: new Date(Date.now() - 24 * 3600 * 1000).toISOString(),
      lat: 15.5,
      lon: 118.0,
      wind_ms: 26.0,
      pressure_hpa: 990.0,
      intensity: 'STS',
      source: 'NCHMF',
      wind_kmh: 94,
      beaufort_level: 10,
    },
    {
      timestamp: new Date(Date.now() - 12 * 3600 * 1000).toISOString(),
      lat: 15.8,
      lon: 115.5,
      wind_ms: 33.0,
      pressure_hpa: 980.0,
      intensity: 'TY',
      source: 'NCHMF',
      wind_kmh: 119,
      beaufort_level: 12,
    },
    {
      timestamp: new Date().toISOString(),
      lat: 16.2,
      lon: 113.8, // In the maritime zone of Hoang Sa archipelago
      wind_ms: 38.0,
      pressure_hpa: 970.0,
      intensity: 'TY',
      source: 'NCHMF',
      wind_kmh: 137,
      beaufort_level: 13,
    },
  ],
  forecast: {
    forecast_id: 'fc-sim-002',
    storm_id: 'WP202601',
    issue_time: new Date().toISOString(),
    generated_at: new Date().toISOString(),
    model_version: 'Direct-Seq2Seq-v2.1',
    model_kind: 'trained-model',
    dataset_version: 'operational-live-2026',
    sources: ['NCHMF', 'CMA', 'JTWC'],
    uncertainty_method: 'Calibrated Quantile Radial Envelope (p80)',
    warnings: [
      'Bão di chuyển vào vùng biển Quần đảo Hoàng Sa (Việt Nam). Gió giật cấp 14-15 gần tâm bão.',
      'Dự báo hướng vào vùng biển các tỉnh Trung Bộ: Thừa Thiên Huế, Đà Nẵng, Quảng Nam, Quảng Ngãi.',
    ],
    disclaimer: 'Chi tham khao; khong thay the ban tin NCHMF.',
    points: [
      {
        horizon_hours: 6,
        valid_time: new Date(Date.now() + 6 * 3600 * 1000).toISOString(),
        lat: 16.4,
        lon: 112.5, // Directly passing Paracel Islands (Hoàng Sa)
        intensity: 'TY',
        radius_km: 30.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(16.4, 112.5, 30.0)],
        },
        wind_ms: 40.0,
        pressure_hpa: 965.0,
      },
      {
        horizon_hours: 12,
        valid_time: new Date(Date.now() + 12 * 3600 * 1000).toISOString(),
        lat: 16.5,
        lon: 111.0,
        intensity: 'STY',
        radius_km: 50.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(16.5, 111.0, 50.0)],
        },
        wind_ms: 43.0,
        pressure_hpa: 960.0,
      },
      {
        horizon_hours: 24,
        valid_time: new Date(Date.now() + 24 * 3600 * 1000).toISOString(),
        lat: 16.4,
        lon: 109.2, // Off the coast of Da Nang - Hue
        intensity: 'TY',
        radius_km: 80.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(16.4, 109.2, 80.0)],
        },
        wind_ms: 36.0,
        pressure_hpa: 975.0,
      },
      {
        horizon_hours: 48,
        valid_time: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
        lat: 16.2,
        lon: 107.8, // Coastline of Thua Thien Hue - Da Nang
        intensity: 'STS',
        radius_km: 130.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(16.2, 107.8, 130.0)],
        },
        wind_ms: 28.0,
        pressure_hpa: 988.0,
      },
      {
        horizon_hours: 72,
        valid_time: new Date(Date.now() + 72 * 3600 * 1000).toISOString(),
        lat: 15.9,
        lon: 106.0, // Moving inland towards Central Laos / Tay Nguyen border
        intensity: 'TD',
        radius_km: 190.0,
        cone: {
          type: 'Polygon',
          coordinates: [generateCircleRing(15.9, 106.0, 190.0)],
        },
        wind_ms: 16.0,
        pressure_hpa: 1002.0,
      },
    ],
  },
};

// 3. Official Comparison Data (S10: Compare AI Model vs NCHMF Official Guidance)
export const MOCK_OFFICIAL_COMPARISON = [
  { horizon_hours: 6, lat: 16.35, lon: 112.4, agency: 'NCHMF' },
  { horizon_hours: 12, lat: 16.42, lon: 110.8, agency: 'NCHMF' },
  { horizon_hours: 24, lat: 16.30, lon: 109.0, agency: 'NCHMF' },
  { horizon_hours: 48, lat: 16.05, lon: 107.5, agency: 'NCHMF' },
  { horizon_hours: 72, lat: 15.70, lon: 105.8, agency: 'NCHMF' },
];

export const MOCK_STORMS_LIST: ActiveTyphoonItem[] = [
  MOCK_STORM_YAGI,
  MOCK_STORM_SIM,
];
