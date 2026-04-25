from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        city = query.get('city', ['London'])[0]

        # Step 1: Get coordinates for the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_req = urllib.request.urlopen(geo_url)
        geo_data = json.loads(geo_req.read().decode())

        if "results" not in geo_data:
            response = {"error": f"City '{city}' not found"}
        else:
            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            country = geo_data["results"][0]["country"]

            # Step 2: Get weather using coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_req = urllib.request.urlopen(weather_url)
            weather_data = json.loads(weather_req.read().decode())
            current = weather_data["current_weather"]

            response = {
                "city": city,
                "country": country,
                "temperature_c": current["temperature"],
                "windspeed_kmh": current["windspeed"],
                "condition": "Sunny" if current["weathercode"] == 0 else "Cloudy/Rainy"
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
