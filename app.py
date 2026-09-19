from main import app, HTML_CONTENT

if __name__ == "__main__":
    import sys
    import streamlit.web.cli as stcli
    sys.argv = [
        "streamlit", "run", "dashboard/app.py",
        "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"
    ]
    sys.exit(stcli.main())
