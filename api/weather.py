from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            amount = query.get('amount', ['1'])[0]
            from_cur = query.get('from', ['USD'])[0].upper()
            to_cur = query.get('to', ['INR'])[0].upper()

            # Call Frankfurter API
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_cur}&to={to_cur}"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read().decode())

            if "rates" not in data or to_cur not in data["rates"]:
                response = {"error": "Invalid currency code. Try USD, INR, EUR, GBP, JPY"}
            else:
                converted = data["rates"][to_cur]
                response = {
                    "from": from_cur,
                    "to": to_cur,
                    "amount": float(amount),
                    "converted": round(converted, 2),
                    "rate": round(converted / float(amount), 4)
                }

        except Exception as e:
            response = {"error": str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
