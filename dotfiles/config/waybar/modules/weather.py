#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request

# ================= 配置区域语言 / Configuration =================
# Language: "zh-CN", "en-SG" for Metric (摄氏度), "en-US" for Imperial (华氏度)
LOCALE = "zh-CN"

# Set your LOCATION_ID, or read WEATHER_LOCATION_ID from environment variables.
# Go to https://weather.com and choose your location, you can see the LOCATION_ID in the URL.
LOCATION_ID = (
    os.getenv("WEATHER_LOCATION_ID")
    or "4bb49c3c2c97f9382266e4d40650e30ee931d0227e19947ffc456deab0db58d7"
)

# ==========================================================

# Define Language Pack
TRANSLATIONS = {
    "zh": {
        "feels_like": "体感温度",
        "low_high": "低 ~ 高",
        "wind": "风速",
        "humidity": "湿度",
        "dew_point": "露点",
        "pressure": "气压",
        "visibility": "能见度",
        "uv_index": "紫外线",
        "hourly_forecast": "每小时预报",
        "daily_forecast": "每日预报",
    },
    "en": {
        "feels_like": "Feels Like",
        "low_high": "Low ~ High",
        "wind": "Wind",
        "humidity": "Humidity",
        "dew_point": "Dew Point",
        "pressure": "Pressure",
        "visibility": "Visibility",
        "uv_index": "UV Index",
        "hourly_forecast": "Hourly Forecast",
        "daily_forecast": "Daily Forecast",
    },
}

# Determine language key based on LOCALE
LANG_KEY = "zh" if LOCALE.lower().startswith("zh") else "en"
LABELS = TRANSLATIONS[LANG_KEY]

# Nerd Font - Weather Icons Mapping (nf-weather-*)
WEATHER_ICONS = {
    "0": "",
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "6": "",
    "7": "",
    "8": "",
    "9": "",
    "10": "",
    "11": "",
    "12": "",
    "13": "",
    "14": "",
    "15": "",
    "16": "",
    "17": "",
    "18": "",
    "19": "",
    "20": "",
    "21": "",
    "22": "",
    "23": "",
    "24": "",
    "25": "",
    "26": "",
    "27": "",
    "28": "",
    "29": "",
    "30": "",
    "31": "",
    "32": "",
    "33": "",
    "34": "",
    "35": "",
    "36": "",
    "37": "",
    "38": "",
    "39": "",
    "40": "",
    "41": "",
    "42": "",
    "43": "",
    "44": "",
    "45": "",
    "46": "",
    "47": "",
}

# Moon Phases
MOON_PHASES = {
    # English
    "New Moon": "",
    "Waxing Crescent": "",
    "First Quarter": "",
    "Waxing Gibbous": "",
    "Full Moon": "",
    "Waning Gibbous": "",
    "Last Quarter": "",
    "Waning Crescent": "",
    # Chinese
    "新月": "",
    "蛾眉月": "",
    "上弦月": "",
    "盈凸月": "",
    "满月": "",
    "亏凸月": "",
    "下弦月": "",
    "残月": "",
}


def get_weather_class(icon_code):
    """根据天气代码返回 CSS 类名，用于动态着色"""
    code = int(icon_code)
    if code in [0, 1, 2, 3, 4, 37, 38, 47]:
        return "stormy"
    if code in [5, 6, 7, 8, 13, 14, 15, 16, 25, 41, 42, 43, 46]:
        return "snowy"
    if code in [9, 10, 11, 12, 17, 18, 35, 39, 40, 45]:
        return "rainy"
    if code in [19, 20, 21, 22]:
        return "foggy"
    if code in [23, 24]:
        return "windy"
    if code in [26, 27, 28, 29, 30]:
        return "cloudy"
    if code in [31, 33]:
        return "night"
    if code in [32, 34, 36]:
        return "sunny"
    return "default"


def get_data():
    url = f"https://weather.com/{LOCALE}/weather/today/l/{LOCATION_ID}?par=google"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        },
    )

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        print(json.dumps({"text": "Error", "tooltip": str(e)}))
        sys.exit(1)

    pattern = re.compile(r'window\.__data\s*=\s*JSON\.parse\("((?:[^"\\]|\\.)*)"\);')
    match = pattern.search(html)

    if not match:
        print(json.dumps({"text": "Error", "tooltip": "Data not found"}))
        sys.exit(1)

    try:
        json_str = match.group(1).encode("utf-8").decode("unicode_escape")
        data = json.loads(json_str)
    except Exception:
        json_str = match.group(1)
        data = json.loads(json_str)

    return data["dal"]


def format_tooltip(dal_data):
    try:
        obs_key = next(
            k for k in dal_data if k.startswith("getSunV3CurrentObservationsUrlConfig")
        )
        hourly_key = next(
            (k for k in dal_data if k.startswith("getSunV3HourlyForecastUrlConfig")),
            None,
        )
        daily_key = next(
            k
            for k in dal_data
            if k.startswith("getSunV3DailyForecastWithHeadersUrlConfig")
        )

        current = dal_data[obs_key][list(dal_data[obs_key].keys())[0]]["data"]
        hourly = (
            dal_data[hourly_key][list(dal_data[hourly_key].keys())[0]]["data"]
            if hourly_key
            else None
        )
        daily = dal_data[daily_key][list(dal_data[daily_key].keys())[0]]["data"]
    except (StopIteration, KeyError, IndexError):
        return {"text": "Error", "tooltip": "Parsing Error", "class": "weather"}

    # --- Current Weather ---
    temp = current.get("temperature", 0)
    feels_like = current.get("temperatureFeelsLike", 0)
    phrase = current.get("wxPhraseLong", "")
    icon_code = str(current.get("iconCode", 44))
    icon = WEATHER_ICONS.get(icon_code, "")

    # Get CSS Class for Waybar
    weather_class = get_weather_class(icon_code)

    high_temp = daily["temperatureMax"][0]
    low_temp = daily["temperatureMin"][0]

    # Details
    wind_speed = current.get("windSpeed", 0)
    wind_dir = current.get("windDirectionCardinal", "")
    humidity = current.get("relativeHumidity", 0)
    pressure = current.get("pressureMeanSeaLevel", 0)
    visibility = current.get("visibility", 0)
    uv_index = current.get("uvIndex", 0)
    uv_desc = current.get("uvDescription", "")
    dew_point = current.get("temperatureDewPoint", 0)

    # Sun & Moon
    sunrise = daily.get("sunriseTimeLocal", [""])[0][11:16]
    sunset = daily.get("sunsetTimeLocal", [""])[0][11:16]

    m_phase_name = daily.get("moonPhase", [""])[0]
    m_icon = ""
    for key, val in MOON_PHASES.items():
        if key in m_phase_name:
            m_icon = val
            break

    # --- Build Tooltip ---
    # Header
    tt = f"<span size='20pt'>{icon}</span>  <span size='x-large' weight='bold'>{phrase}</span>\t"
    tt += f"<span size='16pt'></span>  <span size='x-large' weight='bold'>{temp}°</span>\n"
    # feels like and high/low
    tt += f"{LABELS['feels_like']}\t<span color='#9ccfd8'>{feels_like}°</span>\n"
    tt += f"{LABELS['low_high']}\t<span color='#9ccfd8'>{low_temp}° ~ {high_temp}°</span>\n"

    # separator
    tt += f"<span color='#6e6a86'>{'-' * 50}</span>\n"
    tt += f"<span color='#f6c177'>  {sunrise} -   {sunset}</span>\t"
    tt += f"<span color='#c4a7e7'>{m_icon}  {m_phase_name}</span>\n"

    # Grid Details
    tt += f"  {LABELS['wind']}\t<span color='#ebbcba'>{wind_dir} {wind_speed} km/h</span>\t"
    tt += f"  {LABELS['humidity']}\t<span color='#ebbcba'>{humidity}%</span>\n"

    tt += f"  {LABELS['dew_point']}\t<span color='#ebbcba'>{dew_point}°</span>\t"
    tt += f"  {LABELS['pressure']}\t<span color='#ebbcba'>{pressure} mb</span>\n"

    tt += f"  {LABELS['visibility']}\t<span color='#ebbcba'>{visibility} km</span>\t"
    tt += f"  {LABELS['uv_index']}\t<span color='#ebbcba'>{uv_index} ({uv_desc})</span>\n"

    # Hourly Forecast Section
    if hourly:
        tt += f"<span color='#31748f' weight='bold'>{LABELS['hourly_forecast']}</span> <span color='#6e6a86'>{'-' * 40}</span>\n"
        # Show first 5 available periods
        hourly_limit = 8
        for i in range(min(len(hourly["temperature"]), hourly_limit)):
            # Time: "2025-12-12T15:00:00+0800" -> "15:00"
            time_str = hourly["validTimeLocal"][i][11:16]
            t_val = hourly["temperature"][i]
            precip = hourly["precipChance"][i]
            w_phrase = hourly["wxPhraseLong"][i]
            if w_phrase is None:
                w_phrase = ""  # Handle NoneType
            w_icon_code = str(hourly["iconCode"][i])
            w_icon = WEATHER_ICONS.get(w_icon_code, "")

            tt += f"{time_str}\t<span color='#ebbcba'>{t_val:>3}°</span> <span color='#9ccfd8'> {precip:>2}%</span>\t"
            tt += f"<span color='#e0def4'>{w_icon}  {w_phrase}</span>\n"

    # Daily Forecast Section
    tt += f"<span color='#31748f' weight='bold'>{LABELS['daily_forecast']}</span> <span color='#6e6a86'>{'-' * 40}</span>\n"
    if "daypart" in daily and len(daily["daypart"]) > 0:
        dp = daily["daypart"][0]
        # Show first 8 available periods
        count = 0
        for i in range(len(dp["daypartName"])):
            if count >= 8:
                break

            name = dp["daypartName"][i]
            if not name:
                continue

            t_val = dp["temperature"][i]
            w_phrase = dp["wxPhraseLong"][i]
            w_icon_code = str(dp["iconCode"][i])
            w_icon = WEATHER_ICONS.get(w_icon_code, "")
            precip = dp["precipChance"][i]

            # temperature and precipitation %
            tt += f"{name}\t<span color='#ebbcba'>{t_val:>3}°</span> <span color='#9ccfd8'> {precip:>2}%</span>\t"
            tt += f"<span color='#e0def4'>{w_icon}  {w_phrase}</span>\n"
            count += 1

    return {
        "text": f"{icon} {temp}°",
        "tooltip": tt.rstrip(),
        "class": f"weather {weather_class}",
        "alt": phrase,
    }


if __name__ == "__main__":
    dal_data = get_data()
    print(json.dumps(format_tooltip(dal_data), ensure_ascii=False))
