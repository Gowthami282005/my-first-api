from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the free Jokes API
        url = "https://official-joke-api.appspot.com/random_joke"
        req = urllib.request.urlopen(url)
        joke_data = json.loads(req.read().decode())

        # Build our response
        response = {
            "setup": joke_data["setup"],
            "punchline": joke_data["punchline"],
            "type": joke_data["type"]
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
