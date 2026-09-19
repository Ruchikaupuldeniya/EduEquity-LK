"""
EduEquity LK - Primary Application Entrypoint
Integrates root access and delegates to the Streamlit dashboard.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = str(Path(__file__).resolve().parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# If invoked directly via python app.py or CLI
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    sys.argv = [
        "streamlit",
        "run",
        "dashboard/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ]
    sys.exit(stcli.main())
else:
    # When imported by WSGI/serverless runners, execute dashboard logic
    pass
