document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('analysis-form');
  const results = document.getElementById('results');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const file = formData.get('file');

    if (!file || file.size === 0) {
      results.innerHTML = '<p>Please choose a file.</p>';
      return;
    }

    results.innerHTML = '<p>Analyzing...</p>';

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const payload = await response.json();

      if (!response.ok) {
        results.innerHTML = `<p>Error: ${payload.detail || 'Unknown error'}</p>`;
        return;
      }

      const findings = payload.findings || [];
      let html = `
        <h2>Analysis summary</h2>
        <p>Authorities found: ${payload.authorities_found ?? 0}</p>
        <p>Warnings: ${(payload.warnings || []).join(', ') || 'None'}</p>
        <pre>${(payload.report_text || '').replace(/</g, '&lt;')}</pre>
      `;

      findings.forEach((finding) => {
        html += `
          <div class="finding">
            <h3>${finding.headline}</h3>
            <p><strong>Category:</strong> ${finding.category}</p>
            <p><strong>Severity:</strong> ${finding.severity}</p>
            <p><strong>Purpose provenance:</strong> ${finding.purpose_provenance}</p>
            <p><strong>Explanation:</strong> ${finding.explanation}</p>
            <p><strong>Counterargument:</strong> ${finding.strongest_counterargument}</p>
          </div>
        `;
      });

      results.innerHTML = html;
    } catch (error) {
      results.innerHTML = `<p>Request failed: ${error.message}</p>`;
    }
  });
});
