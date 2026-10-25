import argparse
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time
import requests

from bottle import Bottle, request, response, static_file, run

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PowerScraperWeb")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
SRC_DIR = BASE_DIR / "src"
UI_PATH = SRC_DIR / "ui.html"
REMOTE_URL_FILE = BASE_DIR / "remote_url.txt"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

app = Bottle()


@app.hook('after_request')
def enable_cors():
    """Allow requests from remote origins over ngrok."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'


INJECTOR_PATH = SRC_DIR / "injector.js"


@app.route('/hud.js')
def serve_hud():
    """Serves injector.js dynamically configured with the current host's snapshot endpoint."""
    response.content_type = 'application/javascript; charset=utf-8'
    if not INJECTOR_PATH.is_file():
        response.status = 404
        return '// injector.js not found'

    with open(INJECTOR_PATH, 'r', encoding='utf-8') as f:
        js = f.read()

    host_url = request.urlparts.scheme + "://" + request.urlparts.netloc
    prefix = f"window.__PIERRE_API_ENDPOINT__ = '{host_url}/api/snapshot';\n"
    return prefix + js


@app.route('/')
def index():
    """Serve the Pierre's Power Scraper remote launcher and bookmarklet setup page."""
    host_url = request.urlparts.scheme + "://" + request.urlparts.netloc
    bookmarklet_code = (
        f"javascript:(function(){{"
        f"const s=document.createElement('script');"
        f"s.src='{host_url}/hud.js?t='+Date.now();"
        f"document.body.appendChild(s);"
        f"}})();"
    )
    ogw_url = (
        "https://opengridworks.com/power-plants"
        "?lat=44.8&lng=-74.2&z=7.0"
        "&layers=tx,datacenters,hpoints,rowTx,rowSubs&panel=closed"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pierre's Power Scraper — Office Remote Access</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0a0d14;
      color: #e2e8f0;
      margin: 0;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .container {{
      max-width: 680px;
      width: 100%;
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 32px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    h1 {{
      font-size: 22px;
      color: #f8fafc;
      margin-top: 0;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    h1 span {{ color: #06b6d4; }}
    .badge {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #10b981;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      display: inline-block;
      margin-bottom: 20px;
    }}
    p {{ color: #94a3b8; font-size: 14.5px; line-height: 1.6; margin-bottom: 20px; }}
    .step-box {{
      background: #182234;
      border: 1px solid #27354a;
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 16px;
    }}
    .step-num {{
      color: #06b6d4;
      font-weight: 700;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #0284c7;
      color: #fff;
      padding: 10px 18px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 14px;
      text-decoration: none;
      transition: all 0.2s;
      cursor: grab;
    }}
    .btn:hover {{ background: #0369a1; transform: translateY(-1px); }}
    .btn-green {{ background: #059669; }}
    .btn-green:hover {{ background: #047857; }}
    .note {{
      font-size: 12.5px;
      color: #64748b;
      margin-top: 10px;
      line-height: 1.4;
    }}
    code {{
      background: #1e293b;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: #38bdf8;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">● CONNECTED TO HOME PC</div>
    <h1>Pierre's Power Scraper <span>// Office Remote</span></h1>
    <p>OpenGridWorks blocks embedding inside other websites (<code>X-Frame-Options: DENY</code>). To view the full interactive map at work with zero restrictions, follow these 2 quick steps:</p>

    <div class="step-box">
      <div class="step-num">Step 1 — Drag to Bookmarks Bar</div>
      <p style="margin-bottom: 12px;">Drag this button up to your browser's Bookmarks bar (or right-click and choose "Bookmark this link"):</p>
      <a href="{bookmarklet_code}" class="btn">⚡ Pierre's Power HUD</a>
    </div>

    <div class="step-box">
      <div class="step-num">Step 2 — Launch & Activate Map</div>
      <p style="margin-bottom: 12px;">Open the Canada-US Power Grid map, then simply click your new <strong>⚡ Pierre's Power HUD</strong> bookmark:</p>
      <a href="{ogw_url}" target="_blank" class="btn btn-green">Launch OpenGridWorks ↗</a>
      <div class="note">Once the map loads, clicking your bookmark instantly attaches your custom top bar, all 5 corridor preset buttons, and the <strong>Export Snapshot</strong> button! Snapshots save directly back to your home PC.</div>
    </div>

    <div style="margin-top: 24px; text-align: center;">
      <a href="/api/snapshots" style="color: #06b6d4; font-size: 13px; text-decoration: none;">View Saved Snapshots on Home PC ({RAW_DATA_DIR.name}) ↗</a>
    </div>
  </div>
</body>
</html>
"""



@app.route('/api/snapshot', method=['POST', 'OPTIONS'])
def save_snapshot():
    """Receives corridor snapshot from remote browser and writes to data/raw/."""
    if request.method == 'OPTIONS':
        return {}

    try:
        payload = request.json or {}
        corridor = payload.get("corridor", "snapshot")
        corridor_slug = (
            corridor.replace(" ", "_")
            .replace("➔", "to")
            .replace("/", "-")
            .lower()
        )
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{corridor_slug}_{timestamp}.json"
        target_file = RAW_DATA_DIR / filename

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        logger.info("Saved snapshot from remote client: %s", filename)
        return {
            "status": "success",
            "file": str(target_file),
            "filename": filename
        }
    except Exception as e:
        logger.error("Failed to save snapshot: %s", e)
        response.status = 500
        return {"status": "error", "message": str(e)}


@app.route('/api/snapshots')
def list_snapshots():
    """List all saved snapshots with metadata."""
    snapshots = []
    for p in sorted(RAW_DATA_DIR.glob("*.json"), key=os.path.getmtime, reverse=True):
        snapshots.append({
            "name": p.name,
            "size": p.stat().st_size,
            "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat()
        })
    return {"total": len(snapshots), "snapshots": snapshots}


def start_ngrok(port: int):
    """Checks for existing ngrok tunnel or spawns a new ngrok process."""
    # First, test if ngrok API is already running
    try:
        res = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=1.5)
        if res.status_code == 200:
            data = res.json()
            tunnels = data.get("tunnels", [])
            for t in tunnels:
                if t.get("proto") == "https":
                    return None, t.get("public_url")
    except Exception:
        pass

    # Start new ngrok process
    logger.info("Spawning ngrok tunnel on port %d...", port)
    ngrok_cmd = ["ngrok", "http", str(port)]
    try:
        proc = subprocess.Popen(
            ngrok_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
    except Exception as e:
        logger.warning("Could not automatically spawn ngrok: %s", e)
        return None, None

    # Poll ngrok local API for the public HTTPS URL
    public_url = None
    for _ in range(15):
        time.sleep(1.0)
        try:
            res = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=1.5)
            if res.status_code == 200:
                tunnels = res.json().get("tunnels", [])
                for t in tunnels:
                    if t.get("proto") == "https":
                        public_url = t.get("public_url")
                        break
                if public_url:
                    break
        except Exception:
            continue

    return proc, public_url


def main():
    parser = argparse.ArgumentParser(description="Pierre's Power Scraper - Web Server with ngrok Tunnel")
    parser.add_argument("--port", type=int, default=8055, help="Port to bind (default: 8055)")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--no-tunnel", action="store_true", help="Disable ngrok tunnel launch")
    args = parser.parse_args()

    ngrok_proc = None
    remote_url = None

    if not args.no_tunnel:
        ngrok_proc, remote_url = start_ngrok(args.port)

    # Ensure clean UTF-8 console output on Windows
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    # Banner display
    print("\n" + "=" * 68)
    print(" [POWER] PIERRE'S POWER SCRAPER -- REMOTE WEB SERVER ACTIVE")
    print("=" * 68)
    print(f" LOCAL ACCESS:    http://localhost:{args.port}")
    if remote_url:
        print(f" REMOTE ACCESS:   {remote_url}")
        print(" (Copy this link and open it on your office browser tomorrow!)")
        try:
            with open(REMOTE_URL_FILE, "w", encoding="utf-8") as f:
                f.write(remote_url.strip())
        except Exception:
            pass
    else:
        print(" REMOTE ACCESS:   Tunnel not started (--no-tunnel active).")
    print("=" * 68 + "\n")


    try:
        run(app, host=args.host, port=args.port, quiet=True)
    finally:
        if ngrok_proc:
            logger.info("Stopping background ngrok process...")
            ngrok_proc.terminate()


if __name__ == "__main__":
    main()
