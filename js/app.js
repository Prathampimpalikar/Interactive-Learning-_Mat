/**
 * AlphaMat — Step-by-Step Pathway Application Controller (SPA Router)
 * Landing -> Login -> Dashboard -> Category -> Letter -> Specimen Selection -> 3D Studio
 */

window.App = (function () {
  'use strict';

  // Application State
  const state = {
    currentView: 'landing', // 'landing' | 'login' | 'dashboard' | 'category' | 'letter' | 'selection' | 'viewer'
    mode: 'Animal', // 'Animal' | 'Fruit'
    selectedLetter: 'A',
    activeSpecimen: null,
    isSpeaking: false,
    quiz: {
      currentIndex: 0,
      score: 0,
      streak: 0,
      totalQuestions: 5,
      currentQuestion: null,
      answered: false
    }
  };

  // Web Audio Synth
  const AudioEngine = {
    ctx: null,
    init() {
      if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioCtx();
      }
    },
    playTone(freq = 440, type = 'sine', duration = 0.1, volume = 0.15) {
      try {
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(volume, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
      } catch (e) {}
    },
    playSuccess() {
      this.playTone(523.25, 'triangle', 0.1, 0.15);
      setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.2), 100);
      setTimeout(() => this.playTone(783.99, 'triangle', 0.25, 0.25), 200);
    },
    playError() {
      this.playTone(280, 'sawtooth', 0.15, 0.2);
      setTimeout(() => this.playTone(220, 'sawtooth', 0.25, 0.2), 120);
    },
    playMatStep() {
      this.playTone(380, 'sine', 0.08, 0.25);
      setTimeout(() => this.playTone(580, 'sine', 0.12, 0.2), 60);
    }
  };

  // Helper to fetch dataset items
  function getItemsByMode(mode) {
    if (typeof ALPHAMAT_DATA === 'undefined') return [];
    return mode === 'Animal' ? ALPHAMAT_DATA.animals : ALPHAMAT_DATA.fruits;
  }

  function getItemsByModeAndLetter(mode, letter) {
    const list = getItemsByMode(mode);
    return list.filter(item => item.alphabet === letter);
  }

  function getAllItems() {
    if (typeof ALPHAMAT_DATA === 'undefined') return [];
    return [...ALPHAMAT_DATA.animals, ...ALPHAMAT_DATA.fruits];
  }

  // 13 Multi-Option Mat Blocks (Numbers 0 to 10 on Blocks 1-11, then Alphabet only for 12, 13)
  const MAT_BLOCKS = [
    { id: 1,  gpio: 32, primary: 'A', secondary: 'N', tertiary: '0',  title: 'Block 1' },
    { id: 2,  gpio: 33, primary: 'B', secondary: 'O', tertiary: '1',  title: 'Block 2' },
    { id: 3,  gpio: 25, primary: 'C', secondary: 'P', tertiary: '2',  title: 'Block 3' },
    { id: 4,  gpio: 26, primary: 'D', secondary: 'Q', tertiary: '3',  title: 'Block 4' },
    { id: 5,  gpio: 27, primary: 'E', secondary: 'R', tertiary: '4',  title: 'Block 5' },
    { id: 6,  gpio: 14, primary: 'F', secondary: 'S', tertiary: '5',  title: 'Block 6' },
    { id: 7,  gpio: 12, primary: 'G', secondary: 'T', tertiary: '6',  title: 'Block 7' },
    { id: 8,  gpio: 13, primary: 'H', secondary: 'U', tertiary: '7',  title: 'Block 8' },
    { id: 9,  gpio: 15, primary: 'I', secondary: 'V', tertiary: '8',  title: 'Block 9' },
    { id: 10, gpio: 2,  primary: 'J', secondary: 'W', tertiary: '9',  title: 'Block 10' },
    { id: 11, gpio: 4,  primary: 'K', secondary: 'X', tertiary: '10', title: 'Block 11' },
    { id: 12, gpio: 16, primary: 'L', secondary: 'Y', tertiary: null, title: 'Block 12' },
    { id: 13, gpio: 17, primary: 'M', secondary: 'Z', tertiary: null, title: 'Block 13' }
  ];

  // Navigation Controller (Switching between Views/Slides with URL routing)
  function navigateTo(viewName, pushHash = true) {
    if (!viewName) return;
    if (viewName === 'start') viewName = 'mat';

    state.currentView = viewName;
    const allViews = document.querySelectorAll('.app-view');
    allViews.forEach(v => v.classList.remove('active-view'));

    const target = document.getElementById(`view-${viewName}`);
    if (target) {
      target.classList.add('active-view');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (viewName === 'mat') {
      renderSpaMatBlocks();
    }

    if (pushHash) {
      if (window.location.hash !== `#${viewName}`) {
        history.pushState({ view: viewName }, '', `#${viewName}`);
      }
    }

    AudioEngine.playTone(520, 'sine', 0.06);
  }

  // Render Mat Table Blocks in SPA (3-in-1 for 1-10, 2-letter for 11-13)
  function renderSpaMatBlocks() {
    const grid = document.getElementById('spaMatBlocksGrid');
    if (!grid) return;
    grid.innerHTML = '';

    MAT_BLOCKS.forEach(b => {
      const card = document.createElement('div');
      card.className = 'mat-3in1-card';
      card.id = `spa-mat-block-${b.id}`;
      card.setAttribute('data-gpio', b.gpio);
      const isDual = !b.tertiary;

      card.innerHTML = `
        <div class="mat-card-topbar">
          <span class="mat-block-num">${b.title}</span>
          <span class="mat-gpio-badge">⚡ GPIO ${b.gpio}</span>
        </div>

        <div class="mat-options-row" style="${isDual ? 'grid-template-columns: 1fr 1fr;' : 'grid-template-columns: 1fr 1fr 1fr;'}">
          <div class="mat-option-btn primary-option" onclick="event.stopPropagation(); App.selectMatLetter('${b.primary}', ${b.id}, ${b.gpio});" title="Select Letter ${b.primary}">
            <span class="mat-option-char">${b.primary}</span>
            <span class="mat-option-type">Letter</span>
          </div>
          <div class="mat-option-btn secondary-option" onclick="event.stopPropagation(); App.selectMatLetter('${b.secondary}', ${b.id}, ${b.gpio});" title="Select Letter ${b.secondary}">
            <span class="mat-option-char">${b.secondary}</span>
            <span class="mat-option-type">Letter</span>
          </div>
          ${b.tertiary ? `
          <div class="mat-option-btn tertiary-option" onclick="event.stopPropagation(); App.selectNumber('${b.tertiary}');" title="Open 3D Model of Number ${b.tertiary}">
            <span class="mat-option-char">${b.tertiary}</span>
            <span class="mat-option-type">3D Model</span>
          </div>` : ''}
        </div>

        <div class="mat-card-footer">
          <span>${isDual ? 'Alphabet Only' : 'Touch or Step Pad'}</span>
          <span class="mat-card-action-hint">Choose ${b.primary} →</span>
        </div>
      `;

      card.onclick = () => selectMatLetter(b.primary, b.id, b.gpio);
      grid.appendChild(card);
    });
  }

  // Select Number -> Directly Opens 3D Model Studio
  function selectNumber(num) {
    if (!num) return;
    AudioEngine.playTone(660, 'sine', 0.1);

    const numItem = (ALPHAMAT_DATA.numbers || []).find(n => n.number === String(num) || n.alphabet === String(num));
    if (numItem) {
      openSpecimen(numItem);
    } else {
      window.location.href = `viewer.html?id=number_${encodeURIComponent(num)}&mode=Number&letter=${encodeURIComponent(num)}`;
    }
  }

  // Select Letter from 3-in-1 Mat Block -> Updates Category screen and transitions
  function selectMatLetter(char, blockId = 1, gpio = 32) {
    if (!char) return;
    char = char.toUpperCase();
    state.selectedLetter = char;

    AudioEngine.playMatStep();

    const block = MAT_BLOCKS.find(b => b.primary === char || b.secondary === char) || MAT_BLOCKS[0];
    const cardEl = document.getElementById(`spa-mat-block-${block.id}`);

    if (cardEl) {
      document.querySelectorAll('.mat-3in1-card').forEach(c => c.classList.remove('piezo-triggered'));
      cardEl.classList.add('piezo-triggered');
    }

    const badge = document.getElementById('spaLivePiezoStatusText');
    if (badge) {
      badge.innerHTML = `⚡ Step Detected: <strong>${block.title} (GPIO ${block.gpio})</strong> → Selected <strong>Letter ${char}</strong>!`;
    }

    // Dynamically update Step 2: Category view labels
    const crumbLetter = document.getElementById('spaCrumbSelectedLetter');
    const heroChar = document.getElementById('spaBadgeHeroChar');
    const heroDesc = document.getElementById('spaBadgeHeroDesc');
    const catTitle = document.getElementById('spaCategoryStepTitle');
    const animalLetter = document.getElementById('spaAnimalLetterChar');
    const fruitLetter = document.getElementById('spaFruitLetterChar');
    const btnAnimal = document.getElementById('spaBtnAnimalLabel');
    const btnFruit = document.getElementById('spaBtnFruitLabel');
    const animalDesc = document.getElementById('spaAnimalCardDesc');
    const fruitDesc = document.getElementById('spaFruitCardDesc');

    if (crumbLetter) crumbLetter.textContent = `Letter ${char}`;
    if (heroChar) heroChar.textContent = char;
    if (heroDesc) heroDesc.textContent = `Block ${block.id} • GPIO ${block.gpio} • Letter '${char}' Selected`;
    if (catTitle) catTitle.textContent = `What would you like to explore for Letter ${char}?`;
    if (animalLetter) animalLetter.textContent = char;
    if (fruitLetter) fruitLetter.textContent = char;
    if (btnAnimal) btnAnimal.textContent = `Select Animals for Letter ${char}`;
    if (btnFruit) btnFruit.textContent = `Select Fruits for Letter ${char}`;

    if (typeof ALPHAMAT_DATA !== 'undefined') {
      const animalMatches = (ALPHAMAT_DATA.animals || []).filter(a => a.alphabet === char).map(a => a.name);
      const fruitMatches = (ALPHAMAT_DATA.fruits || []).filter(f => f.alphabet === char).map(f => f.name);

      const animalEx = animalMatches.length > 0 ? ` (e.g. ${animalMatches.slice(0, 2).join(', ')})` : '';
      const fruitEx = fruitMatches.length > 0 ? ` (e.g. ${fruitMatches.slice(0, 2).join(', ')})` : '';

      if (animalDesc) {
        animalDesc.innerHTML = `Explore wildlife species starting with Letter <strong class="text-coral">${char}</strong>${animalEx} with 3D models, lifespans, and superpowers.`;
      }
      if (fruitDesc) {
        fruitDesc.innerHTML = `Discover tropical fruits and berries starting with Letter <strong class="text-coral">${char}</strong>${fruitEx} with vitamin profiles and harvest seasons.`;
      }
    }

    setTimeout(() => {
      navigateTo('category');
    }, 450);
  }

  // Login Handler — Authenticate & Switch to Step 1: 3-in-1 Mat Blocks Table
  function handleLogin(event) {
    if (event) {
      if (typeof event.preventDefault === 'function') event.preventDefault();
      if (typeof event.stopPropagation === 'function') event.stopPropagation();
    }

    const emailEl = document.getElementById('loginEmailInput');
    const pwdEl = document.getElementById('loginPasswordInput');
    const btnSubmit = document.getElementById('btnLoginSubmit');
    const email = emailEl ? emailEl.value.trim() : 'admin';
    const pwd = pwdEl ? pwdEl.value.trim() : 'admin123';

    if (!email || !pwd) {
      AudioEngine.playError();
      return false;
    }

    if (btnSubmit) {
      btnSubmit.disabled = true;
      btnSubmit.innerHTML = `<span>⏳ Signing In...</span>`;
    }

    AudioEngine.playSuccess();

    setTimeout(() => {
      if (btnSubmit) {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = `<span>Login to Explorer Hub</span> <span>→</span>`;
      }
      // Switch directly to Step 1: 3-in-1 Mat Blocks Table Panel
      navigateTo('mat');
    }, 280);

    return false;
  }

  function handleLogout() {
    AudioEngine.playTone(400, 'sine', 0.08);
    navigateTo('landing');
  }

  function fillDemoCredentials() {
    const emailEl = document.getElementById('loginEmailInput');
    const pwdEl = document.getElementById('loginPasswordInput');
    if (emailEl) emailEl.value = 'admin';
    if (pwdEl) pwdEl.value = 'admin123';
    AudioEngine.playTone(600, 'sine', 0.06);
  }

  // Step 2: Select Category (Animal vs Fruit) -> Switches to Step 3: Specimen Selection
  function selectCategory(cat) {
    state.mode = cat;
    AudioEngine.playTone(580, 'sine', 0.06);

    // Update Specimen List Step Header & Breadcrumb
    const selectionTitle = document.getElementById('selectionStepTitle');
    const crumbSelectionCat = document.getElementById('crumbSelectionCat');
    const crumbSelectionLetter = document.getElementById('crumbSelectionLetter');

    if (selectionTitle) selectionTitle.textContent = `${cat}s Starting With '${state.selectedLetter}'`;
    if (crumbSelectionCat) crumbSelectionCat.textContent = `${cat}s`;
    if (crumbSelectionLetter) crumbSelectionLetter.textContent = `Letter ${state.selectedLetter}`;

    renderSpecimenList();

    navigateTo('selection');
  }

  // Step 2 -> Step 3: Select Letter (Triggered by Mat Piezo Step or Click)
  function selectLetter(char, isPiezo = false) {
    selectMatLetter(char);
  }

  // Step 3: Render Specimen List for that letter
  function renderSpecimenList() {
    const grid = document.getElementById('specimenChoiceGrid');
    if (!grid) return;
    grid.innerHTML = '';

    let matching = getItemsByModeAndLetter(state.mode, state.selectedLetter);
    if (matching.length === 0) {
      matching = getAllItems().filter(i => i.alphabet === state.selectedLetter);
    }
    if (matching.length === 0) {
      matching = getItemsByMode(state.mode).slice(0, 4);
    }

    matching.forEach(item => {
      const card = document.createElement('div');
      card.className = 'specimen-select-card';
      const imgSrc = item.hasRealImage && item.image ? `images/${encodeURIComponent(item.image)}` : 'images/alphamat_logo.png';

      card.innerHTML = `
        <div class="specimen-avatar-box">
          <img src="${imgSrc}" alt="${item.name}" onerror="this.src='images/alphamat_logo.png'">
        </div>
        <div class="specimen-card-info">
          <div class="specimen-card-name">${item.name}</div>
          <div class="specimen-card-sci">${item.scientificName || `Letter ${item.alphabet}`}</div>
          <div class="specimen-card-desc">${item.superpower || item.benefits || item.category}</div>
        </div>
        <div style="font-size: 1.2rem; color: var(--coral);">→</div>
      `;

      card.onclick = () => openSpecimen(item);
      grid.appendChild(card);
    });
  }

  // Step 3 -> Step 4: Open 3D Viewer Studio
  function openSpecimen(item) {
    if (!item) return;
    state.activeSpecimen = item;
    AudioEngine.playSuccess();

    // Update Viewer Breadcrumbs
    const crumbViewerCat = document.getElementById('crumbViewerCat');
    const crumbViewerLetter = document.getElementById('crumbViewerLetter');
    const crumbViewerItemName = document.getElementById('crumbViewerItemName');
    const viewerCategoryTag = document.getElementById('viewerCategoryTag');
    const viewerItemTitle = document.getElementById('viewerItemTitle');

    if (crumbViewerCat) crumbViewerCat.textContent = `${state.mode}s`;
    if (crumbViewerLetter) crumbViewerLetter.textContent = `Letter ${item.alphabet}`;
    if (crumbViewerItemName) crumbViewerItemName.textContent = item.name.split(' ')[0];
    if (viewerCategoryTag) viewerCategoryTag.textContent = `${state.mode} 3D AR Model`;
    if (viewerItemTitle) viewerItemTitle.textContent = item.name;

    // Fact Dossier
    const dossierName = document.getElementById('dossierName');
    const dossierSci = document.getElementById('dossierSci');
    const dossierSuperpowerCard = document.getElementById('dossierSuperpowerCard');
    const dossierSuperpowerTitle = document.getElementById('dossierSuperpowerTitle');
    const dossierSuperpowerText = document.getElementById('dossierSuperpowerText');
    const dossierCategory = document.getElementById('dossierCategory');
    const dossierColor = document.getElementById('dossierColor');
    const dossierDiet = document.getElementById('dossierDiet');
    const dossierDietLabel = document.getElementById('dossierDietLabel');
    const dossierLifespan = document.getElementById('dossierLifespan');
    const dossierLifespanLabel = document.getElementById('dossierLifespanLabel');
    const dossierFunFact = document.getElementById('dossierFunFact');

    if (dossierName) dossierName.textContent = item.name;
    if (dossierSci) dossierSci.textContent = item.scientificName || `Alphabet Category: ${item.alphabet}`;

    if (dossierSuperpowerCard) {
      if (state.mode === 'Animal') {
        dossierSuperpowerCard.className = 'superpower-card';
        dossierSuperpowerTitle.innerHTML = '<span>⚡</span> Superpower & Skill';
        dossierSuperpowerText.textContent = item.superpower || 'Special natural adaptations & sensory perception.';
      } else {
        dossierSuperpowerCard.className = 'superpower-card fruit-style';
        dossierSuperpowerTitle.innerHTML = '<span>✨</span> Health Benefits & Nutrients';
        dossierSuperpowerText.textContent = item.benefits || item.vitamins || 'Loaded with natural vitamins & antioxidants.';
      }
    }

    if (dossierCategory) dossierCategory.textContent = item.category || (state.mode === 'Animal' ? 'Fauna' : 'Flora');
    if (dossierColor) dossierColor.textContent = item.color || 'Natural vibrant shade';

    if (state.mode === 'Animal') {
      if (dossierDietLabel) dossierDietLabel.textContent = 'DIET / HABITAT';
      if (dossierDiet) dossierDiet.textContent = item.diet || item.habitat || 'Forests & Woodlands';
      if (dossierLifespanLabel) dossierLifespanLabel.textContent = 'LIFESPAN / WEIGHT';
      if (dossierLifespan) dossierLifespan.textContent = item.lifespan ? `${item.lifespan} (${item.weight || 'Varied'})` : 'Varied';
    } else {
      if (dossierDietLabel) dossierDietLabel.textContent = 'TASTE PROFILE';
      if (dossierDiet) dossierDiet.textContent = item.taste || 'Sweet & refreshing';
      if (dossierLifespanLabel) dossierLifespanLabel.textContent = 'HARVEST SEASON';
      if (dossierLifespan) dossierLifespan.textContent = item.season || 'Seasonal summer';
    }

    if (dossierFunFact) dossierFunFact.textContent = item.funFact || `${item.name} is a key discovery in the AlphaMat curriculum.`;

    // 3D Model Viewer
    const viewer = document.getElementById('studioViewer');
    const loader = document.getElementById('viewerStageLoader');
    const fallback = document.getElementById('viewerImageFallback');
    const fallbackImg = document.getElementById('viewerFallbackImg');

    const btnSpaFs = document.getElementById('btnSpaFullscreen3D');

    if (item.hasRealModel && viewer) {
      if (loader) loader.classList.add('active');
      if (fallback) fallback.classList.remove('active');
      if (btnSpaFs) btnSpaFs.style.display = 'inline-flex';
      viewer.style.display = 'block';
      viewer.src = `model/${encodeURIComponent(item.model)}`;
    } else {
      if (viewer) viewer.style.display = 'none';
      if (loader) loader.classList.remove('active');
      if (fallback) fallback.classList.add('active');
      if (btnSpaFs) btnSpaFs.style.display = 'none';
      const imgSrc = 'images/alphamat_logo.png';
      if (fallbackImg) fallbackImg.src = imgSrc;
    }

    initStudioMatSimulator();
    loadNextQuizQuestion();

    navigateTo('viewer');
  }

  // Direct Start Shortcut from Dashboard
  function startDirectMode(cat, letter) {
    selectCategory(cat);
    selectLetter(letter);
  }

  // Voice Narration
  function speakViewerItem() {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      const btn = document.getElementById('btnViewerSpeak');
      if (btn) btn.innerHTML = '<span>🔊 Listen Audio</span>';
      return;
    }
    if (!state.activeSpecimen) return;

    const item = state.activeSpecimen;
    const text = state.mode === 'Animal'
      ? `${item.name}. Scientific Name: ${item.scientificName || 'Unknown'}. Superpower: ${item.superpower || 'Special skill'}. Fun fact: ${item.funFact || item.description}`
      : `${item.name}. Scientific Name: ${item.scientificName || 'Unknown'}. Health Benefits: ${item.benefits || item.vitamins || 'High nutritional value'}. Fun fact: ${item.funFact || item.description}`;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.92;
    utterance.pitch = 1.05;

    const btn = document.getElementById('btnViewerSpeak');
    utterance.onstart = () => { if (btn) btn.innerHTML = '<span>⏹️ Stop Audio</span>'; };
    utterance.onend = () => { if (btn) btn.innerHTML = '<span>🔊 Listen Audio</span>'; };
    utterance.onerror = () => { if (btn) btn.innerHTML = '<span>🔊 Listen Audio</span>'; };

    window.speechSynthesis.speak(utterance);
  }

  function resetStudioCamera() {
    const viewer = document.getElementById('studioViewer');
    if (viewer) {
      viewer.cameraOrbit = '0deg 75deg 105%';
      if (viewer.resetTurntable) viewer.resetTurntable();
      AudioEngine.playTone(480, 'sine', 0.08);
    }
  }

  function takeStudioSnapshot() {
    const viewer = document.getElementById('studioViewer');
    if (viewer && viewer.style.display !== 'none' && viewer.toDataURL) {
      const link = document.createElement('a');
      link.download = `AlphaMat-${state.activeSpecimen ? state.activeSpecimen.name.replace(/[^a-zA-Z0-9]/g, '_') : '3D'}.png`;
      link.href = viewer.toDataURL('image/png');
      link.click();
      AudioEngine.playSuccess();
    } else {
      alert('Snapshot exported!');
    }
  }

  function openFullscreen3D() {
    if (!state.activeSpecimen || !state.activeSpecimen.model) return;
    const item = state.activeSpecimen;
    const url = `fullscreen.html?model=${encodeURIComponent(item.model)}&title=${encodeURIComponent(item.name)}&category=${encodeURIComponent(state.mode || '3D Studio')}`;
    window.open(url, '_blank');
  }

  // Secondary Tools Subtab Switcher
  function switchStudioSubtab(tabName, btn) {
    document.querySelectorAll('.dash-subtab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    document.querySelectorAll('.dash-tab-content').forEach(tab => tab.style.display = 'none');
    const target = document.getElementById(`studioTab-${tabName}`);
    if (target) target.style.display = 'block';

    AudioEngine.playTone(500, 'sine', 0.06);
  }

  // Mat Simulator
  function initStudioMatSimulator() {
    const grid = document.getElementById('studioNodesGrid');
    if (!grid || grid.children.length > 0) return;

    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    letters.forEach(char => {
      const pad = document.createElement('div');
      pad.className = 'sensor-pad-node';
      pad.innerHTML = `
        <div class="pad-letter">${char}</div>
        <div class="pad-sample">Pad</div>
      `;
      pad.onclick = () => triggerMatSensor(char, pad);
      grid.appendChild(pad);
    });
  }

  function triggerMatSensor(letter, element) {
    AudioEngine.playMatStep();
    element.classList.add('triggered');
    setTimeout(() => element.classList.remove('triggered'), 350);

    const voltage = (3.4 + Math.random() * 1.45).toFixed(2);
    const adcRaw = Math.floor(voltage * 204.8);

    const meterFill = document.getElementById('studioMeterFill');
    if (meterFill) {
      const pct = Math.min(100, Math.floor((voltage / 5.0) * 100));
      meterFill.style.width = `${pct}%`;
    }

    const consoleLogs = document.getElementById('studioTelemetryLogs');
    if (consoleLogs) {
      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
      const logRow = document.createElement('div');
      logRow.className = 'log-entry';
      logRow.innerHTML = `
        <span style="color:#8b9ea3;">[${timeStr}]</span>
        <span style="color:#eb5e41; font-weight:700;">PAD_${letter}</span>
        <span style="color:#279668;">PULSE:${voltage}V (ADC:${adcRaw})</span>
        <span style="color:#c084fc;">FIREBASE:SYNCED</span>
      `;
      consoleLogs.insertBefore(logRow, consoleLogs.firstChild);
      if (consoleLogs.children.length > 25) consoleLogs.removeChild(consoleLogs.lastChild);
    }

    selectLetter(letter);
  }

  // Quiz Engine
  function generateQuizQuestion() {
    const all = getAllItems();
    if (all.length < 4) return null;

    const correctItem = all[Math.floor(Math.random() * all.length)];
    const wrongOptions = [];
    while (wrongOptions.length < 3) {
      const candidate = all[Math.floor(Math.random() * all.length)];
      if (candidate.name !== correctItem.name && !wrongOptions.some(w => w.name === candidate.name)) {
        wrongOptions.push(candidate);
      }
    }

    const questionTypes = ['superpower', 'funfact'];
    const chosenType = questionTypes[Math.floor(Math.random() * questionTypes.length)];

    let questionText = '';
    let categoryTag = '🌟 Discovery Trivia';

    if (chosenType === 'superpower' && correctItem.superpower) {
      categoryTag = '⚡ Superpower & Nutrition';
      questionText = correctItem.type === 'animal'
        ? `Which animal has the superpower: "${correctItem.superpower}"?`
        : `Which fruit is celebrated for: "${correctItem.benefits || correctItem.vitamins}"?`;
    } else {
      categoryTag = '💡 Did You Know?';
      questionText = `Mystery Clue: "${correctItem.funFact || correctItem.description}" — Who is this?`;
    }

    const options = [...wrongOptions, correctItem].sort(() => Math.random() - 0.5);
    return { questionText, categoryTag, correctItem, options };
  }

  function loadNextQuizQuestion() {
    state.quiz.answered = false;
    const fb = document.getElementById('quizFeedbackBox');
    const btnNext = document.getElementById('btnNextQuiz');
    if (fb) fb.classList.remove('active');
    if (btnNext) btnNext.style.display = 'none';

    state.quiz.currentQuestion = generateQuizQuestion();
    if (!state.quiz.currentQuestion) return;

    const q = state.quiz.currentQuestion;
    document.getElementById('quizQuestionText').textContent = q.questionText;
    document.getElementById('quizCategoryTag').textContent = q.categoryTag;
    document.getElementById('quizProgressNum').textContent = `Question ${state.quiz.currentIndex + 1}`;

    const fill = document.getElementById('quizFill');
    if (fill) {
      const pct = Math.min(100, ((state.quiz.currentIndex + 1) / state.quiz.totalQuestions) * 100);
      fill.style.width = `${pct}%`;
    }

    const grid = document.getElementById('quizOptionsGrid');
    if (grid) {
      grid.innerHTML = '';
      const letters = ['A', 'B', 'C', 'D'];
      q.options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.className = 'quiz-option-btn';
        btn.innerHTML = `
          <div style="width:28px; height:28px; border-radius:6px; background:var(--bg-card); display:grid; place-items:center; font-weight:800;">${letters[idx]}</div>
          <span>${opt.name}</span>
        `;
        btn.onclick = () => handleQuizAnswer(opt, btn);
        grid.appendChild(btn);
      });
    }
  }

  function handleQuizAnswer(selectedOption, clickedBtn) {
    if (state.quiz.answered) return;
    state.quiz.answered = true;

    const q = state.quiz.currentQuestion;
    const isCorrect = selectedOption.name === q.correctItem.name;
    const allBtns = document.querySelectorAll('.quiz-option-btn');

    allBtns.forEach(btn => {
      if (btn.querySelector('span').textContent === q.correctItem.name) {
        btn.classList.add('correct');
      }
    });

    const fb = document.getElementById('quizFeedbackBox');
    if (isCorrect) {
      AudioEngine.playSuccess();
      clickedBtn.classList.add('correct');
      state.quiz.score += 20;
      state.quiz.streak += 1;
      if (fb) {
        fb.innerHTML = `<div style="color:#279668; font-weight:800;">🎉 Correct Answer! Stellar Discovery!</div><div>${q.correctItem.funFact || ''}</div>`;
        fb.classList.add('active');
      }
    } else {
      AudioEngine.playError();
      clickedBtn.classList.add('wrong');
      state.quiz.streak = 0;
      if (fb) {
        fb.innerHTML = `<div style="color:#eb5e41; font-weight:800;">❌ The correct answer was ${q.correctItem.name}.</div>`;
        fb.classList.add('active');
      }
    }

    document.getElementById('quizScoreLive').textContent = `${state.quiz.score} pts`;
    document.getElementById('quizStreakLive').textContent = `${state.quiz.streak} 🔥`;
    const btnNext = document.getElementById('btnNextQuiz');
    if (btnNext) btnNext.style.display = 'inline-flex';
  }

  function loadNextQuiz() {
    state.quiz.currentIndex += 1;
    loadNextQuizQuestion();
  }

  // Certificate
  function updateCertificate() {
    const studentName = document.getElementById('studentNameInput').value.trim() || 'Young Explorer';
    const studentClass = document.getElementById('studentClassInput').value.trim();

    document.getElementById('certRecipient').textContent = studentName;
    const classStr = studentClass ? ` from ${studentClass}` : '';
    document.getElementById('certStatement').textContent = `Has successfully mastered the interactive AlphaMat 3D alphabet discovery modules, completed wildlife and botanical curriculum exploration${classStr}, and demonstrated stellar curiosity!`;
  }

  // Theme Toggle
  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    document.querySelectorAll('.theme-toggle').forEach(t => t.textContent = newTheme === 'dark' ? '🌙' : '☀️');
    localStorage.setItem('alphamat_theme', newTheme);
    AudioEngine.playTone(600, 'triangle', 0.08);
  }

  // Init
  function init() {
    const saved = localStorage.getItem('alphamat_theme');
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
      document.querySelectorAll('.theme-toggle').forEach(t => t.textContent = saved === 'dark' ? '🌙' : '☀️');
    }

    // Handle back / forward navigation and hash changes
    window.addEventListener('popstate', () => {
      const hash = window.location.hash.replace('#', '') || 'landing';
      const validViews = ['landing', 'login', 'dashboard', 'mat', 'category', 'letter', 'selection', 'viewer'];
      if (validViews.includes(hash)) {
        navigateTo(hash, false);
      }
    });

    // Check initial URL hash
    const initialHash = window.location.hash.replace('#', '');
    const validViews = ['landing', 'login', 'dashboard', 'mat', 'category', 'letter', 'selection', 'viewer'];
    if (initialHash && validViews.includes(initialHash)) {
      navigateTo(initialHash, false);
    }

    // Physical Mat & Keyboard Listener (Emulates Piezo steps A through Z)
    window.addEventListener('keydown', (e) => {
      // Ignore if user is currently typing in an input field
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;

      const key = e.key.toUpperCase();

      // Number keys 1 & 2 on Category view
      if (state.currentView === 'category') {
        if (key === '1') selectCategory('Animal');
        if (key === '2') selectCategory('Fruit');
      }

      // Alphabet keys A-Z trigger piezo selection on Mat or Letter screen
      if (/^[A-Z]$/.test(key)) {
        if (state.currentView === 'mat') {
          selectMatLetter(key);
        } else if (state.currentView === 'letter') {
          selectLetter(key, true);
        }
      }
    });

    // 📡 Live Hardware Serial Event Listener (Syncs with ESP32 Piezo Mat via hardware_event.json)
    let lastHardwareTimestamp = Date.now() / 1000;
    let initialHardwareCheck = true;

    async function pollHardwareEvent() {
      try {
        const response = await fetch(`hardware_event.json?t=${Date.now()}`, { cache: 'no-store' });
        if (response.ok) {
          const eventData = await response.json();
          if (eventData && eventData.letter && eventData.timestamp) {
            if (initialHardwareCheck) {
              lastHardwareTimestamp = eventData.timestamp;
              initialHardwareCheck = false;
              return;
            }

            if (eventData.timestamp > lastHardwareTimestamp) {
              lastHardwareTimestamp = eventData.timestamp;
              const letter = String(eventData.letter).trim().toUpperCase();
              const gpio = eventData.gpio || 32;
              console.log(`[SPA Hardware Step Detected]: Letter ${letter} (GPIO ${gpio})`);
              if (state.currentView === 'mat') {
                selectMatLetter(letter, 1, gpio);
              }
            }
          }
        }
      } catch (e) {}
    }
    setInterval(pollHardwareEvent, 300);

    // 📡 Live Firebase Realtime Database Listener (Polls for ESP32 hardware step triggers)
    let lastFirebaseLetter = '';
    const FIREBASE_URL = 'https://interactive-mat-b38b8-default-rtdb.firebaseio.com/admin/currentLetter.json';

    async function pollFirebaseLiveStep() {
      try {
        const response = await fetch(FIREBASE_URL, { cache: 'no-store' });
        if (response.ok) {
          const letterVal = await response.json();
          if (letterVal && typeof letterVal === 'string') {
            const letter = letterVal.trim().toUpperCase();
            if (/^[A-Z]$/.test(letter) && letter !== lastFirebaseLetter) {
              lastFirebaseLetter = letter;
              console.log('[Firebase Live Step Detected]:', letter);
              if (state.currentView === 'mat') {
                selectMatLetter(letter);
              } else if (state.currentView === 'letter' || state.currentView === 'category') {
                selectLetter(letter, true);
              }
            }
          }
        }
      } catch (e) {
        // Silent catch for network hiccups
      }
    }
    // Poll Firebase every 500ms
    setInterval(pollFirebaseLiveStep, 500);

    const viewer = document.getElementById('studioViewer');
    if (viewer) {
      viewer.addEventListener('load', () => {
        const loader = document.getElementById('viewerStageLoader');
        if (loader) loader.classList.remove('active');
      });
      viewer.addEventListener('error', () => {
        const loader = document.getElementById('viewerStageLoader');
        if (loader) loader.classList.remove('active');
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Public API
  return {
    navigateTo,
    handleLogin,
    handleLogout,
    fillDemoCredentials,
    selectCategory,
    selectLetter,
    selectMatLetter,
    selectNumber,
    renderSpaMatBlocks,
    openSpecimen,
    startDirectMode,
    speakViewerItem,
    resetStudioCamera,
    takeStudioSnapshot,
    openFullscreen3D,
    switchStudioSubtab,
    loadNextQuiz,
    updateCertificate,
    toggleTheme
  };

})();
