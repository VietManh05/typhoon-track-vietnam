import { CurrentWeather, DailyWeather, HourlyWeather, WeatherLocation } from "../types";
import { VIETNAM_WEATHER_LOCATIONS } from "../data/vietnamLocations";

export const DEMO_WEATHER_LOCATIONS: WeatherLocation[] = VIETNAM_WEATHER_LOCATIONS;
const location = (id: string) => DEMO_WEATHER_LOCATIONS.find((item) => item.id === id) || DEMO_WEATHER_LOCATIONS[0];
const stamp = () => new Date().toISOString();
const metadata = (id: string) => ({ source: "TYPHOON VN Demo", provider: "demo", retrievedAt: stamp(), timezone: "Asia/Ho_Chi_Minh", locationId: id, isStale: false });
export function getDemoWeather(id = "da-nang"): { current: CurrentWeather; hourly: HourlyWeather[]; daily: DailyWeather[] } {
  const place = location(id); const now = Date.now();
  const current: CurrentWeather = { location: place, observationTime: stamp(), temperatureC: 26, feelsLikeC: 28, condition: { code: "rain", label: "Có mưa", icon: "rain" }, humidityPercent: 84, wind: { speedKmh: 18, gustKmh: 29, directionDeg: 70, directionLabel: "Đông Bắc" }, pressureHpa: 1007, visibilityKm: 8, uvIndex: 3, precipitation: { probabilityPercent: 75, rainMm: 3.2 }, metadata: metadata(place.id) };
  const hourly: HourlyWeather[] = Array.from({ length: 12 }, (_, i) => ({ forecastTime: new Date(now + (i + 1) * 3600000).toISOString(), temperatureC: 26 + Math.sin(i / 2) * 2, condition: { code: i < 4 ? "rain" : "partly-cloudy", label: i < 4 ? "Mưa" : "Có mây", icon: i < 4 ? "rain" : "partly" }, precipitation: { probabilityPercent: Math.max(20, 75 - i * 5), rainMm: i < 4 ? 2.1 : 0 }, humidityPercent: 80, wind: { speedKmh: 16 }, metadata: metadata(place.id) }));
  const daily: DailyWeather[] = Array.from({ length: 5 }, (_, i) => ({ forecastDate: new Date(now + i * 86400000).toISOString().slice(0, 10), minTemperatureC: 24 + (i % 2), maxTemperatureC: 29 + (i % 3), condition: { code: i < 2 ? "rain" : "partly-cloudy", label: i < 2 ? "Mưa" : "Có mây", icon: i < 2 ? "rain" : "partly" }, precipitation: { probabilityPercent: i < 2 ? 70 : 35 }, wind: { speedKmh: 14 + i }, metadata: metadata(place.id) }));
  return { current, hourly, daily };
}
