const $ = id => document.getElementById(id);

const mismatch = $('mismatches');
const conservation = $('conservation');
const gc = $('gc');

function sync() {
  $('mismatch-out').value = mismatch.value;
  $('conservation-out').value = Number(conservation.value).toFixed(2);
  $('gc-out').value = Number(gc.value).toFixed(2);
}

[mismatch, conservation, gc].forEach(x => x.addEventListener('input', sync));
sync();

let latestAnalysis = null;

$('risk-form').addEventListener('submit', async e => {
  e.preventDefault();
  const payload = {
    mismatches: +mismatch.value,
    pam_correct: $('pam').checked,
    in_exon: $('exon').checked,
    conservation_score: +conservation.value,
    gc_content: +gc.value
  };
  $('result-state').textContent = 'ANALYZING…';
  $('risk-label').textContent = 'Running Random Forest';
  try {
    const r = await fetch('/api/analyze', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
    });
    const data = await r.json();
    if (!r.ok) throw Error(data.error || 'Analysis failed');
    latestAnalysis = data;
    $('score').textContent = data.risk_score + '%';
    $('risk-label').textContent = data.label;
    $('risk-copy').textContent = `${data.model} evaluated this synthetic profile with ${data.confidence}% confidence. Educational signal only.`;
    $('result-state').textContent = 'ANALYSIS COMPLETE';
    $('impact-mismatch').textContent = data.feature_importance.mismatches > .2 ? 'HIGH' : 'LOW';
    $('impact-pam').textContent = data.feature_importance.pam_correct > .1 ? 'HIGH' : 'LOW';
    $('impact-exon').textContent = data.feature_importance.in_exon > .1 ? 'MEDIUM' : 'LOW';
    $('impact-conservation').textContent = data.feature_importance.conservation_score > .1 ? 'MEDIUM' : 'LOW';
    $('score-ring').style.background = `radial-gradient(circle at center,var(--panel) 58%,transparent 59%),conic-gradient(var(--cyan) 0 ${data.risk_score}%,#18313b ${data.risk_score}% 100%)`;
    updateDashboard(data);
    $('report-btn').disabled = false;
  } catch (err) {
    $('result-state').textContent = 'ERROR';
    $('risk-label').textContent = 'Analysis unavailable';
    $('risk-copy').textContent = err.message;
  }
});

function setMeter(id, value) {
  const el = $(id);
  if (el) el.style.width = `${Math.max(0, Math.min(100, Number(value) || 0))}%`;
}

async function updateDashboard(genetic) {
  const geneticScore = Number(genetic.risk_score) || 0;
  $('dash-genetic').textContent = `${geneticScore}%`;
  setMeter('genetic-meter', geneticScore);
  $('insight-title').textContent = `${genetic.label} genetic signal detected.`;
  $('insight-copy').textContent = `Model confidence is ${genetic.confidence}%. Ecological and governance context should be reviewed before interpreting the signal.`;

  try {
    const ecoResponse = await fetch('/api/ecological-risk', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({gene_drive: false, off_target_sites: Math.max(1, Number(mismatch.value)), population_impact: conservation.value, uncertainty: .35})
    });
    const eco = await ecoResponse.json();
    if (ecoResponse.ok) {
      const ecoScore = Number(eco.score ?? eco.risk_score ?? eco.ecological_score ?? 0);
      $('dash-eco').textContent = `${Math.round(ecoScore)}%`;
      setMeter('eco-meter', ecoScore);
    }
  } catch (_) {}

  try {
    const regResponse = await fetch('/api/regulatory-assessment', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({genetic_score: geneticScore, ecological_score: Number($('dash-eco').textContent) || 0, ethical_flags: 2})
    });
    const reg = await regResponse.json();
    if (regResponse.ok) {
      const regScore = Number(reg.score ?? reg.readiness_score ?? reg.regulatory_score ?? 0);
      $('dash-reg').textContent = `${Math.round(regScore)}%`;
      setMeter('reg-meter', regScore);
    }
  } catch (_) {}
}

// Scenario Simulator: the original page rendered buttons but did not attach handlers.
const scenarioData = {
  baseline: {score: 32, genetic: 30, eco: 25, reg: 34, text: 'Reference conditions with moderate uncertainty and no gene-drive signal.'},
  offtarget: {score: 71, genetic: 78, eco: 63, reg: 76, text: 'Elevated unintended-site activity increases genetic and governance pressure.'},
  drive: {score: 84, genetic: 66, eco: 94, reg: 88, text: 'Gene-drive propagation raises population-level ecological concern and monitoring needs.'},
  conserved: {score: 62, genetic: 54, eco: 72, reg: 69, text: 'High conservation sensitivity increases ecological significance and review requirements.'}
};

function applyScenario(name) {
  const s = scenarioData[name] || scenarioData.baseline;
  document.querySelectorAll('.scenario').forEach(button => button.classList.toggle('active', button.dataset.scenario === name));
  $('scenario-score').textContent = `${s.score}%`;
  $('scenario-copy').textContent = s.text;
  $('sim-genetic-text').textContent = `${s.genetic}%`;
  $('sim-eco-text').textContent = `${s.eco}%`;
  $('sim-reg-text').textContent = `${s.reg}%`;
  setMeter('sim-genetic', s.genetic);
  setMeter('sim-eco', s.eco);
  setMeter('sim-reg', s.reg);
}

document.querySelectorAll('.scenario').forEach(button => {
  button.addEventListener('click', () => applyScenario(button.dataset.scenario));
});
applyScenario('baseline');

// Assessment report generation.
$('report-btn').addEventListener('click', async () => {
  if (!latestAnalysis) return;
  const report = {
    risk: latestAnalysis,
    ecological: {score: Number($('dash-eco').textContent.replace('%','')) || 0},
    regulatory: {score: Number($('dash-reg').textContent.replace('%','')) || 0}
  };
  const response = await fetch('/api/report', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(report)});
  if (!response.ok) return;
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'genova-assessment.pdf';
  link.click();
  URL.revokeObjectURL(url);
});

// Ecological map: dynamically loads Leaflet and provides a graceful visual fallback.
function buildRiskMap() {
  if ($('risk-map-section')) return;
  const section = document.createElement('section');
  section.id = 'risk-map-section';
  section.className = 'section-shell section-block';
  section.innerHTML = `<div class="section-heading"><div><p class="eyebrow"><span></span> ECOLOGICAL RISK MAP</p><h2>Where risk deserves attention.</h2></div><p>Illustrative geographic context for the PBL prototype. Locations are synthetic research zones, not real release sites.</p></div><div class="map-panel panel"><div id="genova-map" class="genova-map"></div><div class="map-legend"><span><i class="legend-low"></i>Lower signal</span><span><i class="legend-mid"></i>Review zone</span><span><i class="legend-high"></i>Higher signal</span></div></div>`;
  const dashboard = $('dashboard');
  dashboard.parentNode.insertBefore(section, dashboard.nextSibling);

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  document.head.appendChild(css);
  const script = document.createElement('script');
  script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  script.onload = () => {
    const map = L.map('genova-map', {scrollWheelZoom: false}).setView([20, 15], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; OpenStreetMap contributors'}).addTo(map);
    const zones = [
      [28, 77, 'Synthetic Zone A', 'Lower signal · conservation proxy 0.42'],
      [0, 30, 'Synthetic Zone B', 'Review zone · population-impact proxy 0.61'],
      [-25, 135, 'Synthetic Zone C', 'Higher signal · ecological sensitivity 0.84'],
      [35, -100, 'Synthetic Zone D', 'Review zone · uncertainty proxy 0.57']
    ];
    zones.forEach(([lat, lng, name, detail]) => L.circleMarker([lat, lng], {radius: 9, weight: 2, fillOpacity: .72}).addTo(map).bindPopup(`<strong>${name}</strong><br>${detail}`));
  };
  document.body.appendChild(script);
}

buildRiskMap();
