"""
EduEquity LK - Application Entrypoint
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HTML_CONTENT = """<!DOCTYPE html>
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
        .card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 5px solid #1E3A8A;
            border-radius: 16px;
            padding: 40px;
            max-width: 650px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.06);
            text-align: center;
        }
        h1 { font-size: 1.85rem; font-weight: 800; color: #1E3A8A; margin-bottom: 12px; }
        p { font-size: 1rem; color: #475569; line-height: 1.6; margin-bottom: 24px; }
        .btn {
            display: inline-block;
            background: #0D9488;
            color: white;
            padding: 14px 28px;
            border-radius: 10px;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
        }
    </style>
</head>
<body>
    <div class="card">
        <div style="background: #FEF3C7; color: #92400E; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 14px;">
            🇱🇰 EduEquity LK Observatory
        </div>
        <h1>Sri Lanka Education Inequality & Dropout Observatory</h1>
        <p>
            Portfolio-grade data science project analyzing school dropout rates across Sri Lanka's 25 administrative districts (2014–2024), with a focus on estate sector disparities.
        </p>
        <a class="btn" href="https://github.com/Ruchikaupuldeniya/EduEquity-LK" target="_blank">
            ⭐ View Repository on GitHub
        </a>
    </div>
</body>
</html>
"""

def app(environ, start_response):
    """WSGI standard callable for Python serverless runtimes."""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [HTML_CONTENT.encode('utf-8')]

# For direct CLI execution (Streamlit dashboard)
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    sys.argv = [
        "streamlit", "run", "dashboard/app.py",
        "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"
    ]
    sys.exit(stcli.main())
