const LOCATIONS = [
    ["ha-noi", "Hà Nội", 21.0278, 105.8342],
    ["hue", "Huế", 16.4637, 107.5909, "Thừa Thiên Huế"],
    ["hai-phong", "Hải Phòng", 20.8449, 106.6881, "Hải Dương"],
    ["da-nang", "Đà Nẵng", 16.0544, 108.2022, "Quảng Nam"],
    ["can-tho", "Cần Thơ", 10.0452, 105.7469, "Hậu Giang", "Sóc Trăng"],
    ["ho-chi-minh", "TP. Hồ Chí Minh", 10.8231, 106.6297, "Sài Gòn", "Bình Dương", "Bà Rịa - Vũng Tàu", "Vũng Tàu"],
    ["lai-chau", "Lai Châu", 22.3862, 103.4703],
    ["dien-bien", "Điện Biên", 21.3860, 103.0230],
    ["son-la", "Sơn La", 21.3256, 103.9188],
    ["lang-son", "Lạng Sơn", 21.8537, 106.7610],
    ["cao-bang", "Cao Bằng", 22.6666, 106.2640],
    ["tuyen-quang", "Tuyên Quang", 21.8236, 105.2140, "Hà Giang"],
    ["lao-cai", "Lào Cai", 22.4856, 103.9707, "Yên Bái"],
    ["thai-nguyen", "Thái Nguyên", 21.5942, 105.8482, "Bắc Kạn"],
    ["phu-tho", "Phú Thọ", 21.3227, 105.4019, "Vĩnh Phúc", "Hòa Bình", "Việt Trì"],
    ["bac-ninh", "Bắc Ninh", 21.1861, 106.0763, "Bắc Giang"],
    ["hung-yen", "Hưng Yên", 20.6464, 106.0511, "Thái Bình"],
    ["quang-ninh", "Quảng Ninh", 21.0064, 107.2925, "Hạ Long"],
    ["ninh-binh", "Ninh Bình", 20.2506, 105.9745, "Hà Nam", "Nam Định"],
    ["thanh-hoa", "Thanh Hóa", 19.8067, 105.7852],
    ["nghe-an", "Nghệ An", 18.6796, 105.6813, "Vinh"],
    ["ha-tinh", "Hà Tĩnh", 18.3559, 105.8877],
    ["quang-tri", "Quảng Trị", 16.8163, 107.1003, "Quảng Bình", "Đồng Hới", "Đông Hà"],
    ["quang-ngai", "Quảng Ngãi", 15.1205, 108.7923, "Kon Tum"],
    ["gia-lai", "Gia Lai", 13.9833, 108.0000, "Bình Định", "Pleiku", "Quy Nhơn"],
    ["dak-lak", "Đắk Lắk", 12.6667, 108.0500, "Phú Yên", "Buôn Ma Thuột", "Tuy Hòa"],
    ["khanh-hoa", "Khánh Hòa", 12.2388, 109.1967, "Ninh Thuận", "Nha Trang", "Phan Rang"],
    ["lam-dong", "Lâm Đồng", 11.9404, 108.4583, "Đắk Nông", "Bình Thuận", "Đà Lạt", "Phan Thiết"],
    ["dong-nai", "Đồng Nai", 10.9574, 106.8427, "Bình Phước", "Biên Hòa"],
    ["tay-ninh", "Tây Ninh", 11.3352, 106.1099, "Long An"],
    ["dong-thap", "Đồng Tháp", 10.4559, 105.6342, "Tiền Giang", "Cao Lãnh", "Mỹ Tho"],
    ["vinh-long", "Vĩnh Long", 10.2396, 105.9572, "Bến Tre", "Trà Vinh"],
    ["an-giang", "An Giang", 10.3759, 105.4185, "Kiên Giang", "Phú Quốc", "Long Xuyên", "Rạch Giá"],
    ["ca-mau", "Cà Mau", 9.1769, 105.1524, "Bạc Liêu"],
].map(([id, name, latitude, longitude, ...aliases]) => ({
    id,
    name,
    province: name,
    country: "VN",
    latitude,
    longitude,
    timezone: "Asia/Ho_Chi_Minh",
    providerLocationId: null,
    aliases,
}));

const normalize = (value) => value
    .toLocaleLowerCase("vi")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d");

const condition = (rawCode) => {
    const code = Number(rawCode);
    if (code === 0) return { code: `wmo-${code}`, label: "Trời quang", icon: "clear-day" };
    if ([1, 2].includes(code)) return { code: `wmo-${code}`, label: "Có mây rải rác", icon: "partly-cloudy" };
    if (code === 3) return { code: `wmo-${code}`, label: "Nhiều mây", icon: "cloudy" };
    if ([45, 48].includes(code)) return { code: `wmo-${code}`, label: "Sương mù", icon: "fog" };
    if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) {
        return { code: `wmo-${code}`, label: "Có mưa", icon: "rain" };
    }
    if ([95, 96, 99].includes(code)) return { code: `wmo-${code}`, label: "Mưa dông", icon: "thunderstorm" };
    return { code: `wmo-${code}`, label: "Thời tiết biến đổi", icon: "cloudy" };
};

const metadata = (location) => ({
    source: "Open-Meteo forecast API",
    provider: "open-meteo",
    retrievedAt: new Date().toISOString(),
    timezone: location.timezone,
    locationId: location.id,
    sourceUrl: "https://open-meteo.com/",
    isStale: false,
});

const at = (values, index) => values?.[index] ?? null;

async function loadForecast(location, sections) {
    const params = new URLSearchParams({
        latitude: String(location.latitude),
        longitude: String(location.longitude),
        timezone: location.timezone,
        ...sections,
    });
    const url = `https://api.open-meteo.com/v1/forecast?${params}`;
    for (let attempt = 0; attempt < 2; attempt += 1) {
        const response = await fetch(url, {
            headers: { Accept: "application/json" },
            cf: { cacheTtl: 300, cacheEverything: true },
        });
        if (response.ok) return response.json();
        const retryable = response.status === 429 || response.status >= 500;
        if (!retryable || attempt === 1) {
            throw new Error(`Open-Meteo returned HTTP ${response.status}`);
        }
        await new Promise((resolve) => setTimeout(resolve, 150));
    }
    throw new Error("Open-Meteo unavailable");
}

function currentPayload(location, item) {
    return {
        location,
        observationTime: item.time,
        temperatureC: item.temperature_2m,
        feelsLikeC: item.apparent_temperature,
        condition: condition(item.weather_code),
        humidityPercent: item.relative_humidity_2m,
        wind: {
            speedKmh: item.wind_speed_10m ?? 0,
            gustKmh: item.wind_gusts_10m,
            directionDeg: item.wind_direction_10m,
            directionLabel: null,
        },
        pressureHpa: item.surface_pressure,
        visibilityKm: null,
        dewPointC: null,
        cloudCoverPercent: item.cloud_cover,
        uvIndex: null,
        precipitation: { probabilityPercent: null, rainMm: item.rain ?? item.precipitation ?? 0 },
        airQualityIndex: null,
        metadata: metadata(location),
    };
}

function hourlyPayload(location, hourly) {
    return (hourly.time || []).map((forecastTime, index) => ({
        forecastTime,
        temperatureC: at(hourly.temperature_2m, index),
        feelsLikeC: at(hourly.apparent_temperature, index),
        condition: condition(at(hourly.weather_code, index)),
        precipitation: {
            probabilityPercent: at(hourly.precipitation_probability, index),
            rainMm: at(hourly.rain, index),
        },
        humidityPercent: at(hourly.relative_humidity_2m, index),
        wind: {
            speedKmh: at(hourly.wind_speed_10m, index) ?? 0,
            gustKmh: at(hourly.wind_gusts_10m, index),
            directionDeg: at(hourly.wind_direction_10m, index),
            directionLabel: null,
        },
        pressureHpa: at(hourly.surface_pressure, index),
        uvIndex: at(hourly.uv_index, index),
        metadata: metadata(location),
    }));
}

function dailyPayload(location, daily) {
    return (daily.time || []).map((forecastDate, index) => ({
        forecastDate,
        minTemperatureC: at(daily.temperature_2m_min, index),
        maxTemperatureC: at(daily.temperature_2m_max, index),
        condition: condition(at(daily.weather_code, index)),
        precipitation: {
            probabilityPercent: at(daily.precipitation_probability_max, index),
            rainMm: at(daily.rain_sum, index),
        },
        wind: {
            speedKmh: at(daily.wind_speed_10m_max, index) ?? 0,
            gustKmh: at(daily.wind_gusts_10m_max, index),
            directionDeg: null,
            directionLabel: null,
        },
        sunrise: at(daily.sunrise, index),
        sunset: at(daily.sunset, index),
        metadata: metadata(location),
    }));
}

const errorResponse = (message, status = 503) =>
    Response.json(
        { error: { message } },
        { status, headers: { "Cache-Control": "no-store" } },
    );

const cachedJson = (body, maxAge = 300) =>
    Response.json(body, {
        headers: {
            "Cache-Control": `public, max-age=${maxAge}, s-maxage=${maxAge}`,
        },
    });

export async function onRequestGet({ request, params }) {
    const route = Array.isArray(params.path) ? params.path.join("/") : params.path;
    const url = new URL(request.url);

    if (route === "locations/search") {
        const query = normalize((url.searchParams.get("q") || "").trim());
        const locations = LOCATIONS.filter(
            (item) => !query || normalize([item.id, item.name, item.province, ...item.aliases].join(" ")).includes(query),
        );
        return cachedJson({ locations }, 86400);
    }

    if (route === "nchmf") {
        return Response.json(
            {
                error: {
                    code: "NCHMF_SOURCE_UNAVAILABLE",
                    message:
                        "Nguồn dữ liệu NCHMF trực tiếp chưa được cấu hình. Vui lòng dùng bản tin chính thức tại nchmf.gov.vn.",
                    sourceUrl: "https://nchmf.gov.vn/",
                },
            },
            { status: 503, headers: { "Cache-Control": "no-store" } },
        );
    }

    const location = LOCATIONS.find((item) => item.id === url.searchParams.get("location_id"));
    if (!location) return errorResponse("Weather location not found", 404);

    try {
        if (route === "bundle") {
            const data = await loadForecast(location, {
                current: "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,rain,cloud_cover",
                hourly: "temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m,uv_index",
                daily: "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum,wind_speed_10m_max,wind_gusts_10m_max,sunrise,sunset",
                forecast_hours: "24",
                forecast_days: "7",
            });
            return cachedJson({
                current: currentPayload(location, data.current || {}),
                hourly: hourlyPayload(location, data.hourly || {}),
                daily: dailyPayload(location, data.daily || {}),
            });
        }

        if (route === "current") {
            const data = await loadForecast(location, {
                current: "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,rain,cloud_cover",
            });
            return cachedJson(currentPayload(location, data.current || {}));
        }

        if (route === "hourly") {
            const data = await loadForecast(location, {
                hourly: "temperature_2m,apparent_temperature,relative_humidity_2m,precipitation_probability,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m,uv_index",
                forecast_hours: "24",
            });
            return cachedJson({ forecasts: hourlyPayload(location, data.hourly || {}) });
        }

        if (route === "daily") {
            const data = await loadForecast(location, {
                daily: "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum,wind_speed_10m_max,wind_gusts_10m_max,sunrise,sunset",
                forecast_days: "7",
            });
            return cachedJson({ forecasts: dailyPayload(location, data.daily || {}) }, 3600);
        }

        return errorResponse("Weather endpoint not found", 404);
    } catch (error) {
        return errorResponse(error instanceof Error ? error.message : "Weather provider unavailable");
    }
}
