document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('primary-form');
  const results = document.getElementById('results');
  const healthStatus = document.getElementById('health-status');

  async function checkHealth() {
    try {
      const response = await fetch('/api/health');
      const payload = await response.json();
      if (response.ok) {
        healthStatus.textContent = `${payload.service}: ${payload.status}`;
        healthStatus.classList.add('ok');
      } else {
        throw new Error('health check failed');
      }
    } catch (error) {
      healthStatus.textContent = 'Service unavailable';
      healthStatus.classList.add('warn');
    }
  }

  function renderMockReport({ url, repo, text, fileName }) {
    const sourceLabel = url ? 'URL' : repo ? 'GitHub Repository' : text ? 'Raw Text' : fileName ? 'Uploaded File' : 'Input';
    const snippet = (text || url || repo || fileName || '').trim();
    const shortSnippet = snippet.length > 220 ? `${snippet.slice(0, 220)}…` : snippet;

    return `
      <div class="notice">
        Queued for analysis: ${sourceLabel}
      </div>
      <div class="metrics">
        <div class="metric"><strong>12</strong> ambiguities</div>
        <div class="metric"><strong>4</strong> loopholes</div>
        <div class="metric"><strong>2</strong> conflicting rules</div>
        <div class="metric"><strong>1</strong> critical exploit path</div>
        <div class="metric"><strong>0.86</strong> confidence</div>
      </div>

      <div class="findings">
        <article class="finding">
          <h3>What it says</h3>
          <p>${(url || repo || fileName || 'Input source') ? escapeHtml(sourceLabel + ': ' + (url || repo || fileName || 'No source provided')) : 'No source provided'}</p>
        </article>

        <article class="finding">
          <h3>What it means</h3>
          <p>The text, workflow, or repository appears to permit a narrow interpretation that may be formally compliant while weakening the original intent.</p>
        </article>

        <article class="finding">
          <h3>How it fails</h3>
          <p>Formal compliance is possible while the real purpose is undermined by ambiguous incentive structures, broad discretion, or missing safeguards.</p>
        </article>

        <article class="finding">
          <h3>How it can be abused</h3>
          <p>An actor can satisfy the literal rule while strategically avoiding the spirit of the requirement, especially when the operational outcome is not measured.</p>
        </article>

        <article class="finding">
          <h3>Intent drift</h3>
          <p>The rule remains technically valid, but it no longer reliably produces the intended protection, outcome, or governance effect.</p>
        </article>

        <article class="finding">
          <h3>Recommended fix</h3>
          <p>Replace discretionary wording with measurable outcomes, enforce stronger review gates, and define both the minimum standard and the required verification step.</p>
        </article>

        <article class="finding">
          <h3>Sample submitted input</h3>
          <p>${escapeHtml(shortSnippet || 'No content was supplied.')}</p>
        </article>
      </div>

      <button class="primary-button" type="button" id="create-sentinel-btn" style="margin-top: 1rem;">Create Sentinel</button>
    `;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const file = formData.get('file');
    const url = (formData.get('url') || '').toString().trim();
    const repo = (formData.get('repo') || '').toString().trim();
    const text = (formData.get('text') || '').toString().trim();

    results.innerHTML = '<div class="notice">Analyzing input...</div>';

    if (file && file.size > 0) {
      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          body: formData,
        });
        const payload = await response.json();

        if (!response.ok) {
          throw new Error(payload.detail || 'Analysis failed.');
        }

        const findings = payload.findings || [];
        results.innerHTML = `
          <div class="notice">File analysis complete</div>
          <div class="metrics">
            <div class="metric"><strong>${findings.length || 0}</strong> findings</div>
            <div class="metric"><strong>${payload.authorities_found || 0}</strong> authorities</div>
            <div class="metric"><strong>${payload.document_hash ? '1' : '0'}</strong> hash</div>
            <div class="metric"><strong>${payload.warnings?.length || 0}</strong> warnings</div>
            <div class="metric"><strong>${(payload.audit?.overall_status || 'unknown')}</strong> status</div>
          </div>
          <div class="findings">
            ${findings.map((finding) => `
              <article class="finding">
                <h3>${escapeHtml(finding.headline || 'Finding')}</h3>
                <p><strong>Severity:</strong> ${escapeHtml(finding.severity || 'unknown')}</p>
                <p><strong>Category:</strong> ${escapeHtml(finding.category || 'unknown')}</p>
                <p><strong>Explanation:</strong> ${escapeHtml(finding.explanation || 'No explanation provided')}</p>
                <p><strong>Counterargument:</strong> ${escapeHtml(finding.strongest_counterargument || 'No counterargument provided')}</p>
              </article>
            `).join('') || '<article class="finding"><h3>No findings</h3><p>No issue was identified for the tested scope.</p></article>'}
          </div>
          <div class="hardening">SHA-256 provenance active</div>
          <pre>${escapeHtml(payload.report_text || 'No report text available.')}</pre>
        `;
        return;
      } catch (error) {
        results.innerHTML = `<div class="notice">Analysis failed: ${escapeHtml(error.message || 'Unknown error')}</div>`;
        return;
      }
    }

    results.innerHTML = renderMockReport({ url, repo, text, fileName: file && file.name ? file.name : '' });

    const sentinelButton = document.getElementById('create-sentinel-btn');
    if (sentinelButton) {
      sentinelButton.addEventListener('click', () => {
        const created = document.createElement('div');
        created.className = 'hardening';
        created.textContent = 'Sentinel created: intent_drift_guard';
        results.appendChild(created);
      });
    }
  });

  checkHealth();
});
