import re
import requests
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel

console = Console()

HEADERS = {'User-Agent': 'SkiWeatherApp/1.0 (learning project)'}

#Resort Registry

RESORTS = {
#VT:
    "Jay Peak": (44.9379, -72.5048, "Jay, VT"),
    "Stowe": (44.5304, -72.7817, "Stowe, VT"),
    "Smugglers' Notch": (44.5895, -72.7904, "Jeffersonville, VT"),
    "Bolton Valley": (44.4212, -72.8507, "Bolton Valley, VT"),
    "Burke Mountain": (44.5694, -71.7825, "Burke, VT"),
    "Killington": (43.6042, -72.8204, "Killington, VT"),
    "Pico": (43.6587, -72.8420, "Killington, VT"),
    "Sugarbush": (44.1362, -72.9079, "Sugarbush, VT"),
    "Mad River Glen": (44.2017, -72.9170, "Fayston, VT"),
    "Okemo": (43.4027, -72.7170, "Ludlow, VT"),
    "Stratton": (43.0429, -72.9109, "Stratton, VT"),
    "Mount Snow": (42.9601, -72.9201, "West Dover, VT"),
    "Magic Mountain": (43.2017, -72.7686, "Londonderry, VT"),
    "Bromley": (43.2206, -72.9381, "Peru, VT"),
#NH:
    "Loon": (44.0568, -71.6314, "Lincoln, NH"),
    "Cannon": (44.1565, -71.6984, "Franconia, NH"),
    "Waterville Valley": (43.9613, -71.5037, "Waterville Valley, NH"),
    "Bretton Woods": (44.2590, -71.4380, "Bretton Woods, NH"),
    "Wildcat": (44.2581, -71.2017, "Pinkham Notch, NH"),
    "Attitash": (44.0827, -71.2298, "Bartlett, NH"),
    "Black Mountain NH": (44.2556, -71.3100, "Jackson, NH"),
    "Cranmore": (44.0639, -71.1306, "North Conway, NH"),
    "Ragged Mountain": (43.4842, -71.8450, "Danbury, NH"),
    "Gunstock": (43.6100, -71.3656, "Gilford, NH"),
#ME:
    "Sugarloaf": (45.0314, -70.3131, "Sugarloaf, ME"),
    "Sunday River": (44.4676, -70.8565, "Sunday River, ME"),
    "Saddleback": (44.9447, -70.5045, "Rangeley, ME"),
    "Black Mountain ME": (44.5673, -70.5456, "Rumford, ME"),
    "Shawnee Peak": (44.1626, -70.8142, "Bridgton, ME"),
#MA:
    "Jiminy Peak": (42.5535, -73.2890, "Hancock, MA"),
    "Berkshire East": (42.6206, -72.7470, "Charlemont, MA"),
    "Wachusett": (42.4885, -71.8865, "Princeton, MA"),
    "Butternut": (42.1148, -73.3153, "Great Barrington, MA"),
    "Bousquet": (42.4084, -73.2437, "Pittsfield, MA"),
#CT:
    "Ski Sundown": (41.8237, -72.9526, "Ski Sundown, CT"),
    "Mount Southington": (41.5956, -72.8845, "Plantsville, CT"),
    "Mohawk Mountain": (41.8417, -73.2370, "Cornwall, CT"),
    "Powder Ridge": (41.5024, -72.7245, "Middlefield, CT"),
    "Woodbury Ski Area": (41.5500, -73.2120, "Woodbury, CT"),
}

# Fetching Resort Data

def fetch_forecast(lat, lon):
    try:
        point_data = requests.get(
            f"https://api.weather.gov/points/{lat},{lon}", headers=HEADERS
        ).json()
        forecast_url = point_data['properties']['forecast']
        forecast_data = requests.get(forecast_url, headers=HEADERS).json()
        return forecast_data
    except Exception:
        return None

#Scoring System

def parse_wind_mph(wind_speed_str: str) -> int:
    nums = [int(n) for n in re.findall(r"\d+", wind_speed_str)]
    return max(nums) if nums else 0

def calculate_score(weather_data) -> int:
    periods = weather_data["properties"]["periods"]

    # Target the next daytime period instead of blindly using periods[0]
    p = next(
        (period for period in periods[:4] if period.get("isDaytime", True)),
        periods[0]  # fallback to first period if no daytime found
    )

    temp = p["temperature"]
    wind_mph = parse_wind_mph(p.get("windSpeed", "0 mph"))
    short_fcst = (p.get("shortForecast") or "").lower()
    detailed_fcst = (p.get("detailedForecast") or "").lower()

    score = 100

    if temp <-5: score -=35
    elif temp <5: score -=20
    elif temp >40: score -=40
    elif temp >32: score -=15

    if wind_mph >=35: score -=45
    elif wind_mph >=25: score -=30
    elif wind_mph >=15: score -=15

    if any(t in short_fcst or t in detailed_fcst for t in ["freezing rain", "ice", "glaze"]):
        score -= 55
    if any(t in short_fcst or t in detailed_fcst for t in ["rain", "drizzle", "freezing drizzle"]):
        score -= 40

    if temp > 32:
        if any(t in short_fcst or t in detailed_fcst for t in ["rain", "drizzle", "freezing rain"]):
            score -= 15
    if "sleet" in short_fcst or "sleet" in detailed_fcst:
        score -= 50
    if "snow" in short_fcst or "snow" in detailed_fcst:
        score += 10

    return max(0, min(100, score))

def score_color(score: int) -> str:
    if score >= 80: return "bold green"
    if score >= 60: return "yellow"
    if score >= 40: return "orange3"
    return "bold red"

def score_bar(score: int) -> str:
    filled = round(score/10)
    return "█" * filled + "░" * (10 - filled)

def score_label(score: int) -> str:
    if score >= 80: return "Excellent"
    if score >= 60: return "Good"
    if score >= 40: return "Fair"
    return "Poor"

# Display Forecast for One Resort

def forecast_emoji(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["ice", "glaze"]):                      return "🧊🧊"
    if any(w in t for w in ["sleet", "freezing rain",
                            "freezing drizzle"]):                  return "🌧️🧊"
    if any(w in t for w in ["blizzard", "heavy snow"]):            return "🌨️❄️"
    if any(w in t for w in ["snow shower", "snow"]):               return "❄️❄️"
    if any(w in t for w in ["rain shower", "showers"]):            return "🌧🌧"
    if any(w in t for w in ["rain", "drizzle"]):                   return "🌦️️🌧"
    if any(w in t for w in ["thunderstorm", "tstm"]):              return "⛈️⚡"
    if any(w in t for w in ["fog", "mist", "haze"]):               return "🌫️🌫️"
    if any(w in t for w in ["partly cloudy", "partly sunny"]):     return "🌤️⛅"
    if any(w in t for w in ["mostly cloudy", "overcast"]):         return "☁️☁️"
    if any(w in t for w in ["mostly sunny", "mostly clear"]):      return "☀️🌤️"
    if any(w in t for w in ["sunny", "clear"]):                    return "☀️☀️"
    if any(w in t for w in ["cloudy"]):                            return "☁️☁️"
    if any(w in t for w in ["windy", "breezy"]):                   return "💨💨"
    return "🏔️"

def show_forecast(name, data):
    periods = data['properties']['periods']
    console.print()
    console.print(Panel(
        f"[bold cyan]{name} - Full Forecast[/bold cyan]\n"
        f"[dim]Retreived: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}[/dim]",
        box=box.DOUBLE_EDGE
    ))
    for period in periods[:3]:
        # Using .get() for safer access
        temp = period.get('temperature', 'N/A')
        unit = period.get('temperatureUnit', '')
        wind_speed = period.get('windSpeed', 'N/A')
        wind_direction = period.get('windDirection', '')
        wind = f"{wind_speed} {wind_direction}".strip() if wind_speed != 'N/A' else 'N/A'

        short = period.get('shortForecast', 'N/A')
        detail = period.get('detailedForecast', 'N/A')
        period_name = period.get('name', 'Unnamed Period')
        emoji = forecast_emoji(short)

        console.print(f"[bold white]📅 {period_name}[/bold white]")
        console.print(f"   🌡️ [cyan]{temp}°{unit}[/cyan] 💨 [cyan]{wind}[/cyan]")
        console.print(f" {emoji} {short}")
        console.print(f"   📝 [dim]{detail}[/dim]")
#Main
def main():
    console.print("\n[bold cyan]⛷️  Ski Rank - fetching forecasts...[/bold cyan]")
    results = {}
    with console.status("[dim]Contacting NWS API...[/dim]"):
        for name, (lat, lon, location) in RESORTS.items():
            data = fetch_forecast(lat, lon)
            if data and "properties" in data:
                results[name] = (data, location)

#Ranked List
    ranked = []
    for name, (data, location) in results.items():
        score = calculate_score(data)
        ranked.append((score, name, data, location))
    ranked.sort(reverse=True)

#Print Scoreboard
    table = Table(
        title="Ski Resort Scoreboard",
        box=box.ROUNDED,
        show_lines=False,
        title_style="bold white",
        header_style="bold cyan",
        expand=False,
    )
    table.add_column("Rank",             style="dim", width=6)
    table.add_column("Resort",                        width=20)
    table.add_column("Location",         style="dim", width=23)
    table.add_column("Bar",                           width=13)
    table.add_column("Score",                         width=8, justify="center")
    table.add_column("Rating",                        width=12)
    table.add_column("Current Forecast",              width=27, no_wrap=True)

    for rank, (score, name, data, location) in enumerate(ranked, 1):
        periods = data['properties']['periods']
        p = periods[0]
        short = p.get("shortForecast", "N/A")
        temp = p.get("temperature", "N/A")
        unit = p.get("temperatureUnit", "")
        color = score_color(score)
        bar = score_bar(score)
        table.add_row(
            f"#{rank}",
            f"[bold]{name}[/bold]",
            location,
            f"[{color}]{bar}[/{color}]",
            f"[{color}]{score}[/{color}]",
            f"[dim]{score_label(score)}[/dim]",
            f"{temp}°{unit}  {short}",
        )

    console.print()
    console.print(table)

# Forecast drill-down loop
    resort_names = [name for _, name, _, _ in ranked]
    name_map = {str(i + 1): name for i, name in enumerate(resort_names)}
    name_map.update({n.lower(): n for n in resort_names})

    console.print("\n[dim]Enter a resort name or rank number to see its full forecast, or [bold]q[/bold] to quit.[/dim]")

    while True:
        choice = Prompt.ask("\n[bold cyan]View forecast for[/bold cyan]").strip()

        if choice.lower() in ("q", "quit", "exit"):
            console.print("[dim]Goodbye! Have fun on the slopes ⛷️⛰️[/dim]\n")
            break

# By number or name
        matched = name_map.get(choice) or name_map.get(choice.lower())

        if matched:
            data = next(d for _, n, d, _ in ranked if n == matched)
            show_forecast(matched, data)
        else:
            console.print(f"[red]Couldn't find '[bold]{choice}[/bold]'. Try a name or rank number. [/red]")

if __name__ == "__main__":
    main()