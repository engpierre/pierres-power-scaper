(function() {
  // 1. Auto-Accept "Interconnection Agreement" Modal
  function autoAcceptAgreement() {
    try {
      // Find checkbox or clickable label for terms
      const checkbox = document.querySelector('input[type="checkbox"]');
      if (checkbox && !checkbox.checked) {
        checkbox.click();
      }

      // Find and click the "Accept & continue" button
      const buttons = Array.from(document.querySelectorAll('button'));
      const acceptBtn = buttons.find(b => b.textContent && b.textContent.includes('Accept & continue'));
      if (acceptBtn) {
        acceptBtn.click();
      }

      // Fallback: If modal dialog persists, hide the modal container
      const dialog = document.querySelector('div[role="dialog"]') || document.querySelector('.modal');
      if (dialog && dialog.style.display !== 'none') {
        dialog.style.display = 'none';
      }
    } catch (err) {
      console.warn('Auto-accept routine error:', err);
    }
  }

  // Run immediately and poll briefly for dynamic hydration
  autoAcceptAgreement();
  const agreementObserver = setInterval(() => {
    const buttons = Array.from(document.querySelectorAll('button'));
    const acceptBtn = buttons.find(b => b.textContent && b.textContent.includes('Accept & continue'));
    if (acceptBtn) {
      autoAcceptAgreement();
    } else {
      clearInterval(agreementObserver);
    }
  }, 300);

  // Stop polling after 5 seconds to preserve resources
  setTimeout(() => clearInterval(agreementObserver), 5000);

  // 2. Prevent Duplicate HUD Injections
  if (document.getElementById('pierre-power-hud')) return;

  // 3. Inject Custom Style & HUD Elements
  const style = document.createElement('style');
  style.id = 'pierre-hud-style';
  style.textContent = `
    #pierre-top-bar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 48px;
      background: rgba(10, 13, 20, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #1e293b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .pierre-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      font-size: 14px;
      color: #f8fafc;
    }
    .pierre-brand span { color: #06b6d4; }
    .pierre-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #10b981;
      background: rgba(16, 185, 129, 0.12);
      padding: 3px 10px;
      border-radius: 9999px;
      border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .pierre-dot {
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
    }
    #pierre-sidebar {
      position: fixed;
      top: 48px;
      left: 0;
      bottom: 0;
      width: 310px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(10px);
      border-right: 1px solid #1e293b;
      z-index: 999998;
      overflow-y: auto;
      padding: 14px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .pierre-sec-title {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #94a3b8;
      margin-bottom: 10px;
      font-weight: 700;
    }
    .pierre-card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 10px 12px;
      margin-bottom: 8px;
      cursor: pointer;
      color: #e2e8f0;
      transition: all 0.15s ease-in-out;
    }
    .pierre-card:hover {
      background: #27354a;
      border-color: #06b6d4;
      transform: translateX(3px);
    }
    .pierre-card .title {
      font-size: 12.5px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
    }
    .pierre-card .tickers {
      font-size: 11px;
      color: #06b6d4;
      margin-top: 3px;
      font-weight: 500;
    }
    .pierre-card .desc {
      font-size: 11px;
      color: #94a3b8;
      margin-top: 2px;
    }
    .pierre-btn {
      background: rgba(30, 41, 59, 0.9);
      border: 1px solid #334155;
      color: #38bdf8;
      border-radius: 6px;
      padding: 5px 12px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .pierre-btn:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      transform: translateY(-1px);
    }
    .pierre-btn:active {
      transform: translateY(0);
    }
    .pierre-btn.saved {
      background: rgba(16, 185, 129, 0.2);
      border-color: #10b981;
      color: #10b981;
    }
  `;
  document.head.appendChild(style);

  const container = document.createElement('div');
  container.id = 'pierre-power-hud';
  container.innerHTML = `
    <div id="pierre-top-bar">
      <div class="pierre-brand">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2.5">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
        Pierre's Power Scraper <span>// CAN-US Corridor</span>
      </div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <button id="pierre-export-btn" class="pierre-btn" title="Export current corridor viewport state to Python data/raw folder">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          Export Snapshot
        </button>
        <div class="pierre-badge">
          <div class="pierre-dot"></div>
          ACTIVE TERMINAL
        </div>
      </div>
    </div>

    <div id="pierre-sidebar">
      <div class="pierre-sec-title">Border Intertie Corridors</div>

      <div class="pierre-card" data-lat="44.8" data-lng="-74.2" data-z="7.0">
        <div class="title">Quebec ➔ NY / NE <span>CHPE</span></div>
        <div class="tickers">Hydro-Québec | ES | NEE</div>
        <div class="desc">HVDC link directly to NYC load zone.</div>
      </div>

      <div class="pierre-card" data-lat="43.8" data-lng="-78.8" data-z="7.0">
        <div class="title">Ontario ➔ NYISO / MISO <span>Nuclear</span></div>
        <div class="tickers">H.TO | CEG | BEP-UN.TO</div>
        <div class="desc">Lake Ontario baseload & cross-border ties.</div>
      </div>

      <div class="pierre-card" data-lat="47.2" data-lng="-88.5" data-z="6.2">
        <div class="title">Upper Midwest ➔ MISO <span>Central</span></div>
        <div class="tickers">FTS.TO (ITC) | DTE | XEL</div>
        <div class="desc">Manitoba/Ontario wheeling lines into MISO.</div>
      </div>

      <div class="pierre-card" data-lat="50.8" data-lng="-114.5" data-z="6.5">
        <div class="title">Western Intertie <span>AB/BC ➔ PNW</span></div>
        <div class="tickers">TA.TO | CPX.TO | BC Hydro</div>
        <div class="desc">Pacific NW interties & regional gas peakers.</div>
      </div>

      <div class="pierre-card" data-lat="45.2" data-lng="-66.5" data-z="6.8">
        <div class="title">Atlantic Hub <span>Maritime Link</span></div>
        <div class="tickers">EMA.TO | NPI.TO</div>
        <div class="desc">Maritimes to ISO-NE flow & offshore nodes.</div>
      </div>

      <div class="pierre-sec-title" style="margin-top: 16px;">Macro Preset</div>
      <div class="pierre-card" data-lat="49.0" data-lng="-96.0" data-z="4.8">
        <div class="title">Full Cross-Border Corridor</div>
        <div class="desc">Macro overview: 42°N to 60°N band.</div>
      </div>
    </div>
  `;
  document.body.appendChild(container);

  let activeCorridorName = 'Quebec ➔ NY / NE CHPE';

  // 4. Smooth In-Place Camera Navigation
  document.querySelectorAll('.pierre-card').forEach(card => {
    card.addEventListener('click', () => {
      const lat = card.getAttribute('data-lat');
      const lng = card.getAttribute('data-lng');
      const z = card.getAttribute('data-z');
      const titleEl = card.querySelector('.title');
      if (titleEl) {
        activeCorridorName = titleEl.textContent.trim();
      }
      const layers = 'tx,datacenters,hpoints,rowTx,rowSubs';
      
      const newUrl = `${window.location.pathname}?lat=${lat}&lng=${lng}&z=${z}&layers=${layers}&panel=closed`;
      window.history.pushState({}, '', newUrl);
      window.dispatchEvent(new PopStateEvent('popstate'));
    });
  });

  // 5. Python <-> JS Bridge Snapshot Exporter
  const exportBtn = document.getElementById('pierre-export-btn');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const payload = {
        corridor: activeCorridorName,
        url: window.location.href,
        timestamp: new Date().toISOString(),
        title: document.title
      };

      const onSaveSuccess = () => {
        exportBtn.classList.add('saved');
        exportBtn.innerHTML = `<span>✓ Saved to Home PC</span>`;
        setTimeout(() => {
          exportBtn.classList.remove('saved');
          exportBtn.innerHTML = `
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Export Snapshot
          `;
        }, 2200);
      };

      if (window.pywebview && window.pywebview.api && window.pywebview.api.save_snapshot) {
        window.pywebview.api.save_snapshot(payload).then(onSaveSuccess).catch(err => {
          console.error('[PYWEBVIEW ERROR]', err);
        });
      } else {
        const remoteEndpoint = window.__PIERRE_API_ENDPOINT__ || 'http://localhost:8055/api/snapshot';
        fetch(remoteEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(res => {
          if (res.status === 'success') {
            onSaveSuccess();
          } else {
            alert('Export failed: ' + (res.message || 'unknown error'));
          }
        })
        .catch(err => {
          console.error('[REMOTE API ERROR]', err);
          alert('Network error communicating with home PC.');
        });
      }
    });
  }
})();

