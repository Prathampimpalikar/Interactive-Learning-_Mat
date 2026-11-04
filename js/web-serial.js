/**
 * ==============================================================================
 * AlphaMat — Direct Web Serial USB Controller (ESP32 5-Piezo Mat)
 * ==============================================================================
 * Connects the web application directly to the physical ESP32 AlphaMat over USB-C
 * using the Web Serial API (Chrome / Edge / Opera over HTTPS or localhost).
 *
 * Hardware Pin Mapping (Verified against piezo_controller.ino):
 *   • Pad A: Pin 32 (GPIO 32)
 *   • Pad B: Pin 33 (GPIO 33)
 *   • Pad C: Pin 36 (GPIO 36 / VP Pin / SENSOR_VP)
 *   • Pad D: Pin 34 (GPIO 34)
 *   • Pad E: Pin 35 (GPIO 35)
 *   • Baud Rate: 115200
 *
 * Features:
 *   - Direct browser-to-ESP32 USB connection (zero Python/server dependency)
 *   - Auto-reconnects on page transitions via getPorts() when permission granted
 *   - Multi-chunk & newline stream buffer (handles fragmented serial packets)
 *   - Boot & baseline calibration noise rejection
 *   - Client-side 350ms vibration debounce protection
 *   - Auto-injects responsive status indicator & connect/disconnect controls
 *   - Integrated with mat.html, selection.html, viewer.html, letter.html & index.html
 *   - Full simulation fallback for testing without hardware
 * ==============================================================================
 */

(function () {
  'use strict';

  const CONFIG = {
    baudRate: 115200,
    sessionKey: 'alphamat_serial_active',
    lastLetterKey: 'alphamat_last_letter',
    debounceMs: 350,
    pinMap: {
      'A': 32,
      'B': 33,
      'C': 36,
      'D': 34,
      'E': 35
    },
    bootKeywords: [
      'rst:', 'boot:', 'configsip', 'ready', 'baseline', 'calibrat',
      'alphamat', '=', '---', 'clk', 'cs', 'mode:', 'flash:', 'cpu',
      'chip', 'rom:', 'baud', 'compiled', 'connecting', 'wifi', 'ip'
    ]
  };

  class AlphaMatSerialController {
    constructor() {
      this.port = null;
      this.reader = null;
      this.readableStreamClosed = null;
      this.isConnected = false;
      this.isReading = false;
      this.lastStepTime = 0;
      this.lastStepLetter = '';
      this.incomingBuffer = '';
      this.uiContainer = null;

      this.init();
    }

    isSupported() {
      return ('serial' in navigator);
    }

    init() {
      // Listen for physical device disconnection
      if (this.isSupported()) {
        navigator.serial.addEventListener('disconnect', (event) => {
          console.warn('[AlphaMat WebSerial] USB Device physically disconnected:', event);
          this.handleDisconnect('ESP32 USB cable was unplugged');
        });
      }

      // Check if DOM is ready to inject UI
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => this.onDomReady());
      } else {
        this.onDomReady();
      }
    }

    onDomReady() {
      this.injectStyles();
      this.injectHeaderWidget();
      this.bindKeyboardSimulation();

      // Attempt automatic reconnect if previously connected in this session
      if (this.isSupported() && sessionStorage.getItem(CONFIG.sessionKey) === 'true') {
        this.tryAutoReconnect();
      } else {
        this.updateUIStatus('disconnected');
      }
    }

    injectStyles() {
      if (document.getElementById('alphamat-serial-styles')) return;
      const style = document.createElement('style');
      style.id = 'alphamat-serial-styles';
      style.textContent = `
        .alphamat-serial-pill {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          padding: 5px 12px;
          border-radius: 9999px;
          font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
          font-size: 0.78rem;
          font-weight: 700;
          background: rgba(30, 18, 58, 0.75);
          border: 1px solid rgba(168, 85, 247, 0.35);
          color: #E2E8F0;
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          transition: all 0.25s ease;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
          user-select: none;
        }
        .alphamat-serial-pill:hover {
          border-color: rgba(168, 85, 247, 0.6);
        }
        .alphamat-status-dot {
          width: 9px;
          height: 9px;
          border-radius: 50%;
          background: #94A3B8;
          box-shadow: 0 0 0 rgba(0,0,0,0);
          transition: all 0.25s ease;
          flex-shrink: 0;
        }
        .alphamat-status-dot.connected {
          background: #10B981;
          box-shadow: 0 0 10px #10B981;
          animation: alphamatPulseGreen 2s infinite;
        }
        .alphamat-status-dot.connecting {
          background: #F59E0B;
          box-shadow: 0 0 8px #F59E0B;
          animation: alphamatPulseYellow 1s infinite;
        }
        .alphamat-status-dot.disconnected {
          background: #EF4444;
        }
        .alphamat-status-dot.unsupported {
          background: #F59E0B;
        }
        @keyframes alphamatPulseGreen {
          0%, 100% { box-shadow: 0 0 6px rgba(16, 185, 129, 0.7); transform: scale(1); }
          50% { box-shadow: 0 0 14px rgba(16, 185, 129, 1); transform: scale(1.15); }
        }
        @keyframes alphamatPulseYellow {
          0%, 100% { opacity: 0.6; }
          50% { opacity: 1; }
        }
        .alphamat-serial-btn {
          background: linear-gradient(135deg, #7C3AED, #9333EA);
          color: #ffffff;
          border: none;
          padding: 4px 10px;
          border-radius: 9999px;
          font-size: 0.74rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.2s ease;
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }
        .alphamat-serial-btn:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(147, 51, 234, 0.45);
        }
        .alphamat-serial-btn.btn-disconnect {
          background: rgba(239, 68, 68, 0.2);
          color: #FCA5A5;
          border: 1px solid rgba(239, 68, 68, 0.4);
        }
        .alphamat-serial-btn.btn-disconnect:hover {
          background: rgba(239, 68, 68, 0.35);
          color: #FFFFFF;
        }
        .alphamat-step-badge {
          display: inline-block;
          background: #EB5E41;
          color: #ffffff;
          font-weight: 900;
          padding: 1px 7px;
          border-radius: 6px;
          font-size: 0.72rem;
          margin-left: 2px;
          letter-spacing: 0.5px;
          animation: alphamatPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes alphamatPop {
          0% { transform: scale(0.6); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
        .alphamat-toast-feedback {
          position: fixed;
          bottom: 24px;
          right: 24px;
          z-index: 99999;
          background: rgba(24, 12, 52, 0.94);
          border: 2px solid #EB5E41;
          color: #FFFFFF;
          padding: 12px 18px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 20px rgba(235, 94, 65, 0.4);
          font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
          font-size: 0.9rem;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 10px;
          pointer-events: none;
          transform: translateY(20px);
          opacity: 0;
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .alphamat-toast-feedback.show {
          transform: translateY(0);
          opacity: 1;
        }
        @media (max-width: 600px) {
          .alphamat-serial-pill {
            padding: 4px 8px !important;
            font-size: 0.72rem !important;
            gap: 5px !important;
          }
          #alphamatStatusText {
            display: none !important;
          }
          .alphamat-serial-btn {
            padding: 3px 8px !important;
            font-size: 0.7rem !important;
          }
        }
      `;
      document.head.appendChild(style);
    }

    injectHeaderWidget() {
      // Find candidate navbar container
      const navContainer =
        document.querySelector('.dash-nav-container > div:last-child') ||
        document.querySelector('.header-actions') ||
        document.querySelector('.brand-group')?.parentElement;

      const widget = document.createElement('div');
      widget.id = 'alphamatWebSerialWidget';
      widget.className = 'alphamat-serial-pill';
      widget.innerHTML = `
        <span class="alphamat-status-dot disconnected" id="alphamatStatusDot"></span>
        <span id="alphamatStatusText">AlphaMat Disconnected</span>
        <span id="alphamatLastStep"></span>
        <button type="button" class="alphamat-serial-btn" id="alphamatSerialBtn" title="Connect your ESP32 Mat via USB">
          🔌 Connect Mat
        </button>
      `;

      if (navContainer) {
        navContainer.insertBefore(widget, navContainer.firstChild);
      } else {
        // Fallback: floating top-right pill
        widget.style.position = 'fixed';
        widget.style.top = '12px';
        widget.style.right = '12px';
        widget.style.zIndex = '9999';
        document.body.appendChild(widget);
      }

      this.uiContainer = widget;

      const btn = widget.querySelector('#alphamatSerialBtn');
      if (btn) {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          if (this.isConnected) {
            this.disconnect();
          } else {
            this.requestConnect();
          }
        });
      }
    }

    updateUIStatus(status, message, lastLetter = '') {
      const dot = document.getElementById('alphamatStatusDot');
      const text = document.getElementById('alphamatStatusText');
      const btn = document.getElementById('alphamatSerialBtn');
      const lastBadge = document.getElementById('alphamatLastStep');

      if (!dot || !text || !btn) return;

      dot.className = `alphamat-status-dot ${status}`;

      if (status === 'connected') {
        text.textContent = 'AlphaMat Connected';
        text.title = 'ESP32 USB Active @ 115200 Baud';
        btn.textContent = 'Disconnect';
        btn.className = 'alphamat-serial-btn btn-disconnect';
        btn.title = 'Disconnect USB connection';
      } else if (status === 'connecting') {
        text.textContent = 'Connecting...';
        btn.textContent = 'Connecting...';
        btn.className = 'alphamat-serial-btn';
      } else if (status === 'unsupported') {
        text.textContent = 'Web Serial Unavailable';
        btn.textContent = 'Help';
        btn.className = 'alphamat-serial-btn';
        btn.onclick = () => {
          alert('Web Serial requires Google Chrome or Microsoft Edge on Desktop (Windows, macOS, Linux, ChromeOS) over HTTPS or localhost.\n\nYou can also emulate sensor steps using keyboard keys (A, B, C, D, E) or clicking the virtual pads!');
        };
      } else {
        text.textContent = message || 'AlphaMat Disconnected';
        btn.textContent = '🔌 Connect Mat';
        btn.className = 'alphamat-serial-btn';
        btn.title = 'Click to connect ESP32 USB';
      }

      if (lastLetter && lastBadge) {
        const gpio = CONFIG.pinMap[lastLetter] || '';
        lastBadge.innerHTML = `<span class="alphamat-step-badge" title="Last physical step detected: Letter ${lastLetter} on Pin ${gpio}">⚡ ${lastLetter}</span>`;
      }

      // Also update page-specific status banners if present
      const liveBannerText = document.getElementById('livePiezoStatusText');
      if (liveBannerText) {
        if (status === 'connected') {
          liveBannerText.innerHTML = `🟢 <strong>AlphaMat USB Active (115200 Baud)</strong> — Step on any pad (A–E)`;
        } else if (status === 'disconnected') {
          liveBannerText.innerHTML = `🖲️ Awaiting ESP32 USB Connection or Step (A–E)`;
        }
      }
    }

    async tryAutoReconnect() {
      if (!this.isSupported()) return;
      try {
        const ports = await navigator.serial.getPorts();
        if (ports && ports.length > 0) {
          console.log('[AlphaMat WebSerial] Found previously authorized USB port. Auto-reconnecting...');
          this.port = ports[0];
          await this.openPort(this.port);
        } else {
          sessionStorage.removeItem(CONFIG.sessionKey);
          this.updateUIStatus('disconnected');
        }
      } catch (err) {
        console.warn('[AlphaMat WebSerial] Auto-reconnect skipped:', err);
        sessionStorage.removeItem(CONFIG.sessionKey);
        this.updateUIStatus('disconnected');
      }
    }

    async requestConnect() {
      if (!this.isSupported()) {
        alert('Web Serial API is not supported in this browser.\n\nPlease open this website in Google Chrome or Microsoft Edge on Desktop over HTTPS to use direct USB AlphaMat communication.');
        this.updateUIStatus('unsupported');
        return;
      }

      try {
        this.updateUIStatus('connecting');
        // Request user to select ESP32 COM port
        this.port = await navigator.serial.requestPort();
        await this.openPort(this.port);
      } catch (err) {
        if (err.name === 'NotFoundError') {
          console.log('[AlphaMat WebSerial] User canceled port selection dialog.');
          this.updateUIStatus('disconnected', 'Port Selection Canceled');
        } else {
          console.error('[AlphaMat WebSerial] Connection error:', err);
          alert(`Could not connect to ESP32: ${err.message}\n\nPlease verify:\n1. The USB cable is securely connected.\n2. Arduino Serial Monitor and other terminal programs are CLOSED.\n3. You selected the correct USB/COM port.`);
          this.updateUIStatus('disconnected', 'Connection Failed');
        }
      }
    }

    async openPort(port) {
      try {
        await port.open({ baudRate: CONFIG.baudRate });
        this.isConnected = true;
        sessionStorage.setItem(CONFIG.sessionKey, 'true');
        this.updateUIStatus('connected');
        console.log(`[AlphaMat WebSerial] Successfully opened serial port at ${CONFIG.baudRate} baud!`);
        this.showToast('✅ AlphaMat ESP32 Connected at 115200 baud! Ready for steps.');

        this.readStreamLoop();
      } catch (err) {
        this.isConnected = false;
        sessionStorage.removeItem(CONFIG.sessionKey);
        console.error('[AlphaMat WebSerial] Failed to open port:', err);
        alert(`Failed to open serial port: ${err.message}\n\nTip: Make sure the Arduino IDE Serial Monitor or Python listener is CLOSED, as only one program can access the COM port at a time.`);
        this.updateUIStatus('disconnected', 'Port Busy');
      }
    }

    async readStreamLoop() {
      this.isReading = true;
      const textDecoder = new TextDecoderStream();
      this.readableStreamClosed = this.port.readable.pipeTo(textDecoder.writable);
      this.reader = textDecoder.readable.getReader();

      try {
        while (this.isReading) {
          const { value, done } = await this.reader.read();
          if (done) {
            break;
          }
          if (value) {
            this.handleIncomingChunk(value);
          }
        }
      } catch (err) {
        console.error('[AlphaMat WebSerial] Read stream error:', err);
      } finally {
        this.handleDisconnect('Port stream closed');
      }
    }

    handleIncomingChunk(chunk) {
      this.incomingBuffer += chunk;
      const lines = this.incomingBuffer.split(/\r?\n/);
      // Keep last partial fragment in buffer
      this.incomingBuffer = lines.pop();

      for (const line of lines) {
        this.processLine(line.trim());
      }
    }

    processLine(rawLine) {
      if (!rawLine) return;
      const upper = rawLine.toUpperCase();

      // Filter out ESP32 boot & calibration messages
      for (const kw of CONFIG.bootKeywords) {
        if (upper.includes(kw.toUpperCase())) {
          return;
        }
      }

      // Resolve letter
      let letter = null;

      // 1. Direct single letter (A, B, C, D, E)
      if (/^[A-E]$/.test(upper)) {
        letter = upper;
      }
      // 2. Prefixes e.g. "LETTER: A", "STEP: A", "STEP A", "TAP A"
      else if (upper.startsWith('LETTER:') || upper.startsWith('STEP:') || upper.startsWith('TAP')) {
        const match = upper.match(/[A-E]/);
        if (match) letter = match[0];
      }
      // 3. GPIO numbers e.g. "GPIO 32", "PIN 32", "32"
      else {
        if (upper.includes('32')) letter = 'A';
        else if (upper.includes('33')) letter = 'B';
        else if (upper.includes('36') || upper.includes('VP')) letter = 'C';
        else if (upper.includes('34')) letter = 'D';
        else if (upper.includes('35')) letter = 'E';
      }

      if (letter) {
        this.triggerStepEvent(letter, false);
      }
    }

    triggerStepEvent(letter, isSimulated = false) {
      const now = Date.now();
      // Vibration debounce filter (prevents double-firing from piezo ringing)
      if (now - this.lastStepTime < CONFIG.debounceMs && letter === this.lastStepLetter) {
        return;
      }

      this.lastStepTime = now;
      this.lastStepLetter = letter;
      const gpio = CONFIG.pinMap[letter] || 0;

      const sourceTag = isSimulated ? '[SIMULATED]' : '[PHYSICAL USB]';
      console.log(`%c[AlphaMat WebSerial] ${sourceTag} Step Detected -> Letter: ${letter} (GPIO ${gpio})`, 'color: #10B981; font-weight: bold; font-size: 13px;');

      // Save state
      localStorage.setItem(CONFIG.lastLetterKey, JSON.stringify({ letter, gpio, timestamp: now }));
      this.updateUIStatus(this.isConnected ? 'connected' : 'disconnected', null, letter);

      // Play audio tone if available
      this.playChime(letter);

      // Show toast
      this.showToast(`⚡ Step: Letter <strong>${letter}</strong> (Pin ${gpio}) ${isSimulated ? '<em>[Simulated]</em>' : ''}`);

      // Dispatch global DOM event for any custom listeners
      window.dispatchEvent(new CustomEvent('alphamat:step', {
        detail: { letter, gpio, timestamp: now, isSimulated }
      }));

      // Route event to current page handler
      this.routeStepToCurrentPage(letter, gpio);
    }

    routeStepToCurrentPage(letter, gpio) {
      // 1. mat.html
      if (typeof window.selectLetter === 'function') {
        const blockId = (letter === 'A') ? 1 : (letter === 'B') ? 2 : (letter === 'C') ? 3 : (letter === 'D') ? 4 : (letter === 'E') ? 5 : 1;
        window.selectLetter(letter, blockId, gpio);
        return;
      }

      // 2. selection.html
      const path = window.location.pathname.toLowerCase();
      if (path.includes('selection.html') || window.location.href.includes('selection.html')) {
        const params = new URLSearchParams(window.location.search);
        const currentMode = params.get('mode') || 'Animal';
        const currentLetter = (params.get('letter') || '').toUpperCase();
        if (currentLetter !== letter) {
          console.log(`[AlphaMat Router] Selection screen switching to Letter ${letter} in ${currentMode} mode...`);
          window.location.href = `selection.html?mode=${encodeURIComponent(currentMode)}&letter=${encodeURIComponent(letter)}&gpio=${encodeURIComponent(gpio)}`;
        }
        return;
      }

      // 3. viewer.html
      if (path.includes('viewer.html') || window.location.href.includes('viewer.html')) {
        const params = new URLSearchParams(window.location.search);
        const currentMode = params.get('mode') || 'Animal';
        const currentLetter = (params.get('letter') || '').toUpperCase();
        if (currentLetter !== letter) {
          console.log(`[AlphaMat Router] 3D Viewer loading specimen for Letter ${letter}...`);
          // Navigate to selection screen or load new specimen
          window.location.href = `selection.html?mode=${encodeURIComponent(currentMode)}&letter=${encodeURIComponent(letter)}&gpio=${encodeURIComponent(gpio)}`;
        }
        return;
      }

      // 4. letter.html
      if (path.includes('letter.html') || window.location.href.includes('letter.html')) {
        const params = new URLSearchParams(window.location.search);
        const currentMode = params.get('mode') || 'Animal';
        window.location.href = `selection.html?mode=${encodeURIComponent(currentMode)}&letter=${encodeURIComponent(letter)}&gpio=${encodeURIComponent(gpio)}`;
        return;
      }

      // 5. index.html (Hero virtual mat simulator)
      if (typeof window.stepHeroPad === 'function') {
        window.stepHeroPad(letter);
      }
    }

    playChime(letter) {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        const freqs = { 'A': 440, 'B': 493.88, 'C': 523.25, 'D': 587.33, 'E': 659.25 };
        const freq = freqs[letter] || 500;

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, ctx.currentTime + 0.12);

        gain.gain.setValueAtTime(0.18, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.18);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.18);
      } catch (e) {
        // Audio optional
      }
    }

    showToast(htmlMsg) {
      let toast = document.getElementById('alphamatToastFeedback');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'alphamatToastFeedback';
        toast.className = 'alphamat-toast-feedback';
        document.body.appendChild(toast);
      }
      toast.innerHTML = `<span>⚡</span> <span>${htmlMsg}</span>`;
      toast.classList.add('show');

      if (this._toastTimer) clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 1800);
    }

    async disconnect() {
      this.isReading = false;
      sessionStorage.removeItem(CONFIG.sessionKey);

      if (this.reader) {
        try {
          await this.reader.cancel();
          await this.readableStreamClosed.catch(() => {});
          this.reader.releaseLock();
        } catch (e) {}
        this.reader = null;
      }

      if (this.port) {
        try {
          await this.port.close();
        } catch (e) {}
        this.port = null;
      }

      this.isConnected = false;
      this.updateUIStatus('disconnected');
      this.showToast('AlphaMat USB Disconnected.');
      console.log('[AlphaMat WebSerial] Serial port cleanly disconnected.');
    }

    handleDisconnect(reason) {
      this.isReading = false;
      this.isConnected = false;
      sessionStorage.removeItem(CONFIG.sessionKey);
      this.updateUIStatus('disconnected', 'Disconnected');
      if (reason) {
        console.warn(`[AlphaMat WebSerial] Disconnected: ${reason}`);
        this.showToast(`⚠️ ${reason}`);
      }
    }

    bindKeyboardSimulation() {
      // Global keyboard emulator (A, B, C, D, E) for seamless testing without hardware
      window.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.isComposing) return;
        if (e.ctrlKey || e.altKey || e.metaKey) return;

        const k = e.key.toUpperCase();
        if (['A', 'B', 'C', 'D', 'E'].includes(k)) {
          this.triggerStepEvent(k, true);
        }
      });
    }

    // Public API for testing or scripts
    simulate(letter) {
      const u = String(letter).toUpperCase();
      if (['A', 'B', 'C', 'D', 'E'].includes(u)) {
        this.triggerStepEvent(u, true);
      }
    }
  }

  // Export globally
  window.AlphaMatSerial = new AlphaMatSerialController();
})();
