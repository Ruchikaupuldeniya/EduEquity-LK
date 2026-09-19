"""
EduEquity LK - Vercel Serverless Function Entrypoint
Provides native Vercel Python runtime compatibility.
"""

from http.server import BaseHTTPRequestHandler
import json

HTML_RESPONSE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduEquity LK: Sri Lanka Education Observatory</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #F8FAFC;
            color: #0F172A;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 5px solid #1E3A8A;
            border-radius: 16px;
            padding: 40px;
            max-width: 650px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.06);
            text-align: center;
        }
        h1 {
            font-size: 1.85rem;
            font-weight: 800;
            color: #1E3A8A;
            margin-bottom: 12px;
        }
        p {
            font-size: 1rem;
            color: #475569;
            line-height: 1.6;
            margin-bottom: 24px;
        }
        .btn {
            display: inline-block;
            background: #0D9488;
            color: white;
            padding: 14px 28px;
            border-radius: 10px;
            font-weight: 700;
            text-decoration: none;
            transition: background 0.2s;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
        }
        .btn:hover {
            background: #0F766E;
        }
        .badge {
            background: #FEF3C7;
            color: #92400E;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">🇱🇰 EduEquity LK Observatory</div>
        <h1>Sri Lanka Education Inequality & Dropout Project</h1>
        <p>
            This data science project is built with Python, Plotly, and Streamlit, analyzing 
            school dropout rates across Sri Lanka's 25 administrative districts (2014–2024).
        </p>
        <p>
            <strong>Interactive Live App & Code:</strong><br>
            View the full repository, notebooks, and policy reports on GitHub.
        </p>
        <a class="btn" href="https://github.com/Ruchikaupuldeniya/EduEquity-LK" target="_blank">
            ⭐ View Project on GitHub
        </a>
    </div>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_RESPONSE.encode('utf-8'))
        return

def app(environ, start_response):
    """WSGI standard callable for Python serverless frameworks."""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [HTML_RESPONSE.encode('utf-8')]
