"""Current provincial-level Vietnamese weather locations.

The catalogue follows the 34 provincial-level administrative units effective
from 1 July 2025. Aliases retain former province names after the mergers.
"""

from __future__ import annotations

import unicodedata

from .models import WeatherLocation


def _location(
    id: str,
    name: str,
    latitude: float,
    longitude: float,
    *aliases: str,
    provider_location_id: str | None = None,
) -> WeatherLocation:
    return WeatherLocation(
        id=id,
        name=name,
        province=name,
        latitude=latitude,
        longitude=longitude,
        aliases=list(aliases),
        provider_location_id=provider_location_id,
    )


LOCATIONS = (
    _location("ha-noi", "Hà Nội", 21.0278, 105.8342),
    _location("hue", "Huế", 16.4637, 107.5909, "Thừa Thiên Huế"),
    _location("hai-phong", "Hải Phòng", 20.8449, 106.6881, "Hải Dương"),
    _location(
        "da-nang",
        "Đà Nẵng",
        16.0544,
        108.2022,
        "Quảng Nam",
        provider_location_id="352954",
    ),
    _location("can-tho", "Cần Thơ", 10.0452, 105.7469, "Hậu Giang", "Sóc Trăng"),
    _location(
        "ho-chi-minh",
        "TP. Hồ Chí Minh",
        10.8231,
        106.6297,
        "Sài Gòn",
        "Bình Dương",
        "Bà Rịa - Vũng Tàu",
        "Vũng Tàu",
    ),
    _location("lai-chau", "Lai Châu", 22.3862, 103.4703),
    _location("dien-bien", "Điện Biên", 21.3860, 103.0230),
    _location("son-la", "Sơn La", 21.3256, 103.9188),
    _location("lang-son", "Lạng Sơn", 21.8537, 106.7610),
    _location("cao-bang", "Cao Bằng", 22.6666, 106.2640),
    _location("tuyen-quang", "Tuyên Quang", 21.8236, 105.2140, "Hà Giang"),
    _location("lao-cai", "Lào Cai", 22.4856, 103.9707, "Yên Bái"),
    _location("thai-nguyen", "Thái Nguyên", 21.5942, 105.8482, "Bắc Kạn"),
    _location(
        "phu-tho", "Phú Thọ", 21.3227, 105.4019, "Vĩnh Phúc", "Hòa Bình", "Việt Trì"
    ),
    _location("bac-ninh", "Bắc Ninh", 21.1861, 106.0763, "Bắc Giang"),
    _location("hung-yen", "Hưng Yên", 20.6464, 106.0511, "Thái Bình"),
    _location("quang-ninh", "Quảng Ninh", 21.0064, 107.2925, "Hạ Long"),
    _location("ninh-binh", "Ninh Bình", 20.2506, 105.9745, "Hà Nam", "Nam Định"),
    _location("thanh-hoa", "Thanh Hóa", 19.8067, 105.7852),
    _location("nghe-an", "Nghệ An", 18.6796, 105.6813, "Vinh"),
    _location("ha-tinh", "Hà Tĩnh", 18.3559, 105.8877),
    _location(
        "quang-tri", "Quảng Trị", 16.8163, 107.1003, "Quảng Bình", "Đồng Hới", "Đông Hà"
    ),
    _location("quang-ngai", "Quảng Ngãi", 15.1205, 108.7923, "Kon Tum"),
    _location(
        "gia-lai", "Gia Lai", 13.9833, 108.0000, "Bình Định", "Pleiku", "Quy Nhơn"
    ),
    _location(
        "dak-lak", "Đắk Lắk", 12.6667, 108.0500, "Phú Yên", "Buôn Ma Thuột", "Tuy Hòa"
    ),
    _location(
        "khanh-hoa",
        "Khánh Hòa",
        12.2388,
        109.1967,
        "Ninh Thuận",
        "Nha Trang",
        "Phan Rang",
    ),
    _location(
        "lam-dong",
        "Lâm Đồng",
        11.9404,
        108.4583,
        "Đắk Nông",
        "Bình Thuận",
        "Đà Lạt",
        "Phan Thiết",
    ),
    _location("dong-nai", "Đồng Nai", 10.9574, 106.8427, "Bình Phước", "Biên Hòa"),
    _location("tay-ninh", "Tây Ninh", 11.3352, 106.1099, "Long An"),
    _location(
        "dong-thap", "Đồng Tháp", 10.4559, 105.6342, "Tiền Giang", "Cao Lãnh", "Mỹ Tho"
    ),
    _location("vinh-long", "Vĩnh Long", 10.2396, 105.9572, "Bến Tre", "Trà Vinh"),
    _location(
        "an-giang",
        "An Giang",
        10.3759,
        105.4185,
        "Kiên Giang",
        "Phú Quốc",
        "Long Xuyên",
        "Rạch Giá",
    ),
    _location("ca-mau", "Cà Mau", 9.1769, 105.1524, "Bạc Liêu"),
)
BY_ID = {item.id: item for item in LOCATIONS}


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.casefold().replace("đ", "d"))
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def search_locations(query: str) -> list[WeatherLocation]:
    q = _normalize(query.strip())
    return [
        item
        for item in LOCATIONS
        if not q
        or q in _normalize(" ".join((item.id, item.name, item.province, *item.aliases)))
    ]
