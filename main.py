import argparse
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import sys
import threading
import webview

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PowerScraper")

# Centralized Path Definitions
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
STORAGE_PATH = DATA_DIR / "webview_cache"
INJECTOR_PATH = BASE_DIR / "src" / "injector.js"

# Map position: Focused directly on the Canada / Northern US corridor
INITIAL_URL = (
    "https://opengridworks.com/power-plants"
    "?lat=45.5&lng=-73.6&z=6.5"
    "&layers=tx,datacenters,hpoints,rowTx,rowSubs&panel=closed"
)


class PowerScraperAPI:
    """Python <-> JS Bridge exposed to pywebview window."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_snapshot(self, payload: dict) -> dict:
        """Persist captured map, corridor, or scraped state to disk as JSON."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            corridor_slug = (
                payload.get("corridor", "snapshot")
                .replace(" ", "_")
                .replace("➔", "to")
                .replace("/", "-")
                .lower()
            )
            target_file = self.output_dir / f"{corridor_slug}_{timestamp}.json"
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            logger.info("Saved corridor snapshot: %s", target_file.name)
            return {"status": "success", "file": str(target_file)}
        except Exception as e:
            logger.error("Error saving snapshot: %s", e)
            return {"status": "error", "message": str(e)}

    def log_client_event(self, message: str) -> None:
        """Receive frontend console logs directly inside Python."""
        logger.info("[WebView2 Client] %s", message)


def inject_custom_hud(window):
    """Injects the custom header, corridor presets, and modal handlers."""
    if not INJECTOR_PATH.is_file():
        logger.warning("Injector script not found at expected path: %s", INJECTOR_PATH)
        return

    try:
        with open(INJECTOR_PATH, "r", encoding="utf-8") as f:
            js_payload = f.read()
        window.evaluate_js(js_payload)
        logger.info("Custom HUD successfully injected into WebView2.")
    except Exception as e:
        logger.error("Failed to inject custom HUD: %s", e)


def main():
    parser = argparse.ArgumentParser(description="Pierre's Power Scraper Desktop Client")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Chromium DevTools inspector and verbose debug logging"
    )
    args, _ = parser.parse_known_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Ensure cache and raw output directories exist
    STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize Python <-> JS API Bridge
    scraper_api = PowerScraperAPI(RAW_DATA_DIR)

    window = webview.create_window(
        title="Pierre's Power Scraper — Canada & Northern US",
        url=INITIAL_URL,
        width=1500,
        height=950,
        resizable=True,
        min_size=(1024, 700),
        background_color="#0a0d14",
        js_api=scraper_api
    )

    # Resilient event binding across pywebview versions
    window.events.loaded += lambda *args, **kwargs: inject_custom_hud(window)

    # Graceful exit watchdog to allow WebView2 to flush IndexedDB & session cookies
    def on_closed():
        logger.info("Window closed. Allowing WebView2 to flush storage...")
        timer = threading.Timer(1.5, lambda: os._exit(0))
        timer.daemon = True
        timer.start()

    window.events.closed += on_closed

    # private_mode=False and storage_path preserve all login cookies and session tokens
    webview.start(
        gui="edgechromium",
        debug=args.debug,
        private_mode=False,
        storage_path=str(STORAGE_PATH)
    )


if __name__ == "__main__":
    main()

