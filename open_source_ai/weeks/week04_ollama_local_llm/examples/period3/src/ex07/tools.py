"""모델에게 맡길 함수들. 함수를 추가하면 TOOLS 에도 넣는다."""

from datetime import datetime

import httpx


def get_current_time() -> str:
    """지금 날짜와 시각을 알려 준다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def multiply(a: float, b: float) -> float:
    """두 수를 곱한다.

    Args:
        a: 첫 번째 수
        b: 두 번째 수
    """
    return a * b


def get_weather(city: str) -> str:
    """한국 도시의 지금 날씨(기온, 풍속, 하늘 상태)를 알려 준다.

    Args:
        city: 한국어 도시 이름 (예: 서울, 전주, 부산)
    """
    # Open-Meteo: API 키 없이 쓰는 공개 날씨 API (https://open-meteo.com)
    place = None
    for name in [city, city + "시"]:  # "전주"로 못 찾으면 "전주시"로 다시 찾는다
        found = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": name, "count": 1, "language": "ko", "countryCode": "KR"},
        ).json().get("results")
        if found:
            place = found[0]
            break
    if place is None:
        return f"'{city}' 도시를 찾지 못했다."

    now = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "Asia/Seoul",
        },
    ).json()["current"]
    sky = {0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림", 45: "안개", 61: "비", 63: "비", 65: "강한 비", 71: "눈", 80: "소나기", 95: "뇌우"}
    return (f"{place['name']} {now['time']} 기온 {now['temperature_2m']}°C, "
            f"풍속 {now['wind_speed_10m']} km/h, {sky.get(now['weather_code'], '코드 ' + str(now['weather_code']))}")


TOOLS = {
    "get_current_time": get_current_time, 
    "multiply": multiply, 
    "get_weather": get_weather
}
