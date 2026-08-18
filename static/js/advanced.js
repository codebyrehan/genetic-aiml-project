(() => {
  const $ = id => document.getElementById(id);
  const esc = value => String(value).replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  function section(title, eyebrow, copy, body) {
    const el = document.createElement('section');
    el.className = 'section-shell section-block advanced-section';
    el.innerHTML = `<div class="section-heading"><div><p class="eyebrow"><span></span>${eyebrow}</p><h2>${title}</h2></div><p>${copy}</p></div>${body}`;
    return el;
  }

  function addExplainability() {
    if (!$('analyzer') || $('explainability')) return;
    const el = section('Why did Genova score it this way?', 'EXPLAINABLE AI', 'Feature contribution is shown as a model signal, not causal proof.', `<div id="explainability" class="panel explain-panel"><div class="explain-empty">Run the analyzer to populate feature contributions.</div></div>`);
    $('analyzer').parentNode.insertBefore(el, $('dashboard'));
  }

  function renderExplainability(data) {
    const panel = $('explainability');
    if (!panel || !data?.feature_importance) return;
    const labels = {mismatches:'Mismatch count', pam_correct:'PAM correctness', in_exon:'Exon location', conservation_score:'Conservation score', gc_content:'GC content'};
    const rows = Object.entries(data.feature_importance).sort((a,b) => b[1] - a[1]);
    panel.innerHTML = rows.map(([key,value]) => `<div class="explain-row"><div><strong>${labels[key] || key}</strong><span>${(value * 100).toFixed(1)}% relative importance</span></div><div class="meter"><i style="width:${Math.min(100, value * 100)}%"></i></div></div>`).join('') + `<div class="explain-note"><strong>Interpretation guardrail</strong><span>Feature importance describes how the trained synthetic model uses features. It does not establish biological causation.</span></div>`;
  }

  function addModelLab() {
    if ($('model-lab')) return;
    const el = section('Model Intelligence', 'MODEL PERFORMANCE', 'A deterministic synthetic benchmark makes the ML pipeline inspectable instead of hiding performance behind a single prediction.', `<div id="model-lab" class="model-lab-grid"><div class="panel model-summary"><div class="loading">Loading benchmark…</div></div><div class="panel confusion-panel"><h3>Confusion matrix</h3><div id="confusion-matrix" class="matrix"></div></div></div>`);
    const target = document.querySelector('#patterns');
    target.parentNode.insertBefore(el, target);
    fetch('/api/model-metrics').then(r => r.json()).then(data => {
      if (data.error) throw Error(data.error);
      const m = data.metrics;
      $('model-lab').querySelector('.model-summary').innerHTML = `<div class="metric-grid">${Object.entries(m).map(([k,v]) => `<div><span>${esc(k)}</span><strong>${v}%</strong></div>`).join('')}</div><p class="lab-note">${data.dataset_size.toLocaleString()} synthetic rows · ${data.split} · Random Forest · reproducible seed 42.</p>`;
      const matrix = data.confusion_matrix;
      $('confusion-matrix').innerHTML = `<div class="matrix-head"><span></span><span>Pred 0</span><span>Pred 1</span></div>${matrix.map((row,i) => `<div class="matrix-row"><b>Actual ${i}</b>${row.map(v => `<strong>${v}</strong>`).join('')}</div>`).join('')}`;
    }).catch(err => $('model-lab').querySelector('.model-summary').innerHTML = `<div class="error-state">${esc(err.message)}</div>`);
  }

  function addDatasetStudio() {
    if ($('dataset-studio')) return;
    const el = section('Research Dataset Studio', 'DATASET INTELLIGENCE', 'Profile a CSV locally through the server endpoint. The uploaded file is analyzed in memory and is not persisted by this feature.', `<div id="dataset-studio" class="panel dataset-panel"><div class="upload-row"><label class="upload-control">Choose CSV<input id="dataset-file" type="file" accept=".csv,text/csv"></label><button class="primary-btn" id="profile-dataset" type="button">Profile Dataset →</button><span id="dataset-state">READY</span></div><div id="dataset-output" class="dataset-output"><p>Supported research features: mismatches, PAM correctness, exon location, conservation score and GC content.</p></div></div>`);
    const target = document.querySelector('#patterns');
    target.parentNode.insertBefore(el, target);
    $('profile-dataset').addEventListener('click', async () => {
      const file = $('dataset-file').files[0];
      if (!file) { $('dataset-state').textContent = 'SELECT A CSV'; return; }
      $('dataset-state').textContent = 'PROFILING…';
      const form = new FormData(); form.append('file', file);
      try {
        const response = await fetch('/api/dataset-profile', {method:'POST', body:form});
        const data = await response.json();
        if (!response.ok) throw Error(data.error || 'Profiling failed');
        $('dataset-state').textContent = 'PROFILE COMPLETE';
        $('dataset-output').innerHTML = `<div class="dataset-stats"><div><span>Rows</span><strong>${data.rows.toLocaleString()}</strong></div><div><span>Columns</span><strong>${data.columns}</strong></div><div><span>Supported</span><strong>${data.supported_features.length}</strong></div><div><span>Missing fields</span><strong>${Object.keys(data.missing_values).length}</strong></div></div><div class="dataset-columns"><strong>Columns</strong><span>${data.column_names.map(esc).join(' · ')}</span></div><div class="dataset-columns"><strong>Missing values</strong><span>${Object.keys(data.missing_values).length ? Object.entries(data.missing_values).map(([k,v]) => `${esc(k)}: ${v}`).join(' · ') : 'None detected'}</span></div>`;
      } catch (err) { $('dataset-state').textContent = 'ERROR'; $('dataset-output').innerHTML = `<div class="error-state">${esc(err.message)}</div>`; }
    });
  }

  function addPresentationMode() {
    const button = document.createElement('button');
    button.className = 'presentation-btn'; button.type = 'button'; button.textContent = 'Presentation Mode';
    button.addEventListener('click', () => document.body.classList.toggle('presentation-mode'));
    document.querySelector('.topbar')?.appendChild(button);
  }

  addExplainability();
  addModelLab();
  addDatasetStudio();
  addPresentationMode();

  const form = $('risk-form');
  form?.addEventListener('submit', () => setTimeout(() => renderExplainability(window.latestAnalysis), 500));

  // Observe the analyzer result without changing the existing stable flow.
  const score = $('score');
  if (score) {
    const observer = new MutationObserver(() => {
      const state = {feature_importance: {}};
      ['mismatches','pam_correct','in_exon','conservation_score','gc_content'].forEach(k => state.feature_importance[k] = 0.2);
      if (window.latestAnalysis) renderExplainability(window.latestAnalysis);
    });
    observer.observe(score, {childList:true, characterData:true, subtree:true});
  }
})();
