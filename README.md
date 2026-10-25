# ⚡ Pierre's Power Scraper

A standalone, modular, high-performance scraping and extraction engine.

> **Status:** Initialized & Ready for Architecture  
> **Isolation:** 100% independent project (zero coupling with Hermes or OpenClaw).

---

## 📁 Project Structure

```
pierres_power_scraper/
├── src/                  # Core scraping engine, extractors, pipelines
├── data/                 # Raw & processed data outputs
│   ├── raw/
│   └── processed/
├── logs/                 # Operational & run logs
├── tests/                # Unit and integration test suites
├── .env.example          # Template environment configurations
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
└── main.py               # Main runtime entry point
```

---

## 🚀 How to Run

### 1. Local Desktop App (Native WebView2 Window)
```bash
python main.py
```
*Optional debug inspector:* `python main.py --debug`

### 2. Remote Office Access (Web App + ngrok Tunnel)
To access the exact same interface from your office browser:
```bash
# Option A: Double-click start_remote_web.bat
# Option B: Run PowerShell script
.\start_remote_web.ps1
```
* Once started, the script will display your live **REMOTE ACCESS** link:
  `https://xxxx.ngrok-free.app`
* Open that link in Chrome or Edge on your work computer.
* Clicking **Export Snapshot** in your office browser will save the data directly back onto this home PC in `data/raw/`!

