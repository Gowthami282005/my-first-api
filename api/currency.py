from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        amount = float(query.get('amount', ['1'])[0])
        from_cur = query.get('from', ['USD'])[0].upper()
        to_cur = query.get('to', ['INR'])[0].upper()

        # Call Frankfurter free currency API
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_cur}&to={to_cur}"
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode())

        if "rates" not in data:
            response = {"error": "Invalid currency code"}
        else:
            converted = data["rates"][to_cur]
            response = {
                "from": from_cur,
                "to": to_cur,
                "amount": amount,
                "converted": round(converted, 2),
                "rate": round(converted / amount, 4)
            }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
