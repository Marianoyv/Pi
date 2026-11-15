(function () {
  'use strict';

  const UTM_FIELDS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  const CORE_UTM_FIELDS = ['utm_source', 'utm_medium', 'utm_campaign'];
  const UTM_PRESETS = {
    'linkedin-organic': { source: 'linkedin', medium: 'social', label: 'LinkedIn organic' },
    newsletter: { source: 'newsletter', medium: 'email', label: 'Email newsletter' },
    'google-paid': { source: 'google', medium: 'cpc', label: 'Google paid' },
    'meta-paid': { source: 'meta', medium: 'paid-social', label: 'Meta paid' }
  };
  const FORMAT_RULES = {
    html5: { label: 'HTML5 display', maxWeight: 200, requiresClick: true },
    static: { label: 'Static image', maxWeight: 150, requiresClick: true },
    video: { label: 'Video', maxWeight: 5000, requiresClick: true },
    native: { label: 'Native / social', maxWeight: 300, requiresClick: true },
    other: { label: 'Other', maxWeight: 300, requiresClick: false }
  };
  const TYPE_LABELS = {
    display: 'Display',
    third_party: 'Third-party tag',
    rich_media: 'Rich media',
    other: 'Other'
  };
  const INPUT_LABELS = { html: 'HTML creative', third_party: 'Third-party tag' };

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function normalizePublicUrl(value, required) {
    const trimmed = String(value || '').trim();
    if (!trimmed) {
      if (required) throw new Error('Enter a valid public URL.');
      return '';
    }
    const candidate = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
    let parsed;
    try {
      parsed = new URL(candidate);
    } catch (error) {
      throw new Error('Enter a valid public URL.');
    }
    if (!['http:', 'https:'].includes(parsed.protocol) || !parsed.hostname) {
      throw new Error('Enter a valid public URL.');
    }
    return parsed.toString();
  }

  function normalizeUtmValue(value) {
    return String(value || '')
      .trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/&/g, '-and-')
      .replace(/[^a-z0-9._-]+/g, '-')
      .replace(/-{2,}/g, '-')
      .replace(/^[-_.]+|[-_.]+$/g, '');
  }

  function renderList(items, emptyText) {
    const values = items.length ? items : [emptyText];
    return `<ul class="tool-list">${values.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
  }

  function renderChecklist(items) {
    const labels = { ok: 'OK', warn: 'Review', fail: 'Flag', muted: 'Info' };
    return `<ul class="tool-checklist">${items.map((item) => `
      <li class="tool-checklist__item">
        <div class="tool-checklist__top">
          <strong>${escapeHtml(item.label)}</strong>
          <span class="tool-check-status tool-check-status--${escapeHtml(item.status)}">${labels[item.status] || 'Info'}</span>
        </div>
        <p>${escapeHtml(item.detail)}</p>
      </li>`).join('')}</ul>`;
  }

  function getResultTarget(form) {
    return form.closest('.tool-detail__main')?.querySelector('[data-browser-tool-result]');
  }

  function revealResult(form, html) {
    const target = getResultTarget(form);
    if (!target) return null;
    const main = form.closest('.tool-detail__main');
    main?.querySelectorAll('.tool-empty, [data-browser-tool-placeholder]').forEach((node) => {
      node.hidden = true;
    });
    target.innerHTML = html;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return target;
  }

  function showError(form, message) {
    revealResult(form, `
      <section class="tool-result">
        <article class="tool-result__hero tool-result__hero--critical" role="alert">
          <p class="tools-label">Input needs review</p>
          <h2>Check the entered information</h2>
          <p>${escapeHtml(message)}</p>
        </article>
      </section>`);
  }

  function emitToolEvent(form, eventName, detail = {}) {
    form.dispatchEvent(new CustomEvent(eventName, {
      bubbles: true,
      detail: {
        tool_name: form.dataset.browserTool,
        ...detail
      }
    }));
  }

  function loadExample(form) {
    const payload = form.querySelector('#browser-tool-example');
    if (!payload) return;
    let values;
    try {
      values = JSON.parse(payload.textContent);
    } catch (error) {
      return;
    }
    Object.entries(values).forEach(([name, value]) => {
      const field = form.elements.namedItem(name);
      if (field) field.value = value;
    });
  }

  function applyUtmPreset(form, presetName) {
    const preset = UTM_PRESETS[presetName];
    if (!preset) return;
    const source = form.elements.namedItem('utm_source');
    const medium = form.elements.namedItem('utm_medium');
    const campaign = form.elements.namedItem('utm_campaign');
    if (source) source.value = preset.source;
    if (medium) medium.value = preset.medium;
    form.querySelectorAll('[data-utm-preset]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.utmPreset === presetName));
    });
    const feedback = form.querySelector('[data-utm-preset-feedback]');
    if (feedback) {
      feedback.textContent = `${preset.label} selected: source ${preset.source}, medium ${preset.medium}. Add a specific campaign name.`;
    }
    form.dispatchEvent(new CustomEvent('pi:utm-preset', {
      bubbles: true,
      detail: { preset_name: presetName }
    }));
    campaign?.focus();
  }

  function buildUtmResult(form) {
    const data = new FormData(form);
    const destination = normalizePublicUrl(data.get('destination_url'), true);
    const url = new URL(destination);
    const originalPairs = Array.from(url.searchParams.entries());
    const provided = {};
    const normalizedFields = [];

    UTM_FIELDS.forEach((field) => {
      const rawValue = String(data.get(field) || '').trim();
      const value = normalizeUtmValue(rawValue);
      const input = form.elements.namedItem(field);
      if (input) input.value = value;
      if (value) {
        provided[field] = value;
        url.searchParams.set(field, value);
      }
      if (rawValue && rawValue !== value) normalizedFields.push(field);
    });

    const missing = CORE_UTM_FIELDS.filter((field) => !url.searchParams.get(field));
    const providedCount = Object.keys(provided).length;
    let overview;
    if (!missing.length && !providedCount) {
      overview = ['Already tagged', 'good', 'The destination already included the core UTM parameters. The original query remains intact.'];
    } else if (!providedCount) {
      overview = ['No new campaign tags', 'warn', 'The destination is valid, but no new UTM parameters were supplied.'];
    } else if (!missing.length) {
      overview = ['Ready to use', 'good', 'The final URL includes source, medium and campaign. Optional parameters are added only when supplied.'];
    } else {
      overview = ['Valid URL with missing fields', 'warn', 'The URL was built correctly, but core UTM parameters are still missing.'];
    }

    const rows = UTM_FIELDS.map((field) => {
      const finalValue = url.searchParams.get(field) || '';
      if (provided[field]) return { label: field, value: finalValue, status: 'ok', detail: 'Supplied in this run.' };
      if (finalValue) return { label: field, value: finalValue, status: 'ok', detail: 'Preserved from the destination URL.' };
      if (missing.includes(field)) return { label: field, value: 'Not provided', status: 'warn', detail: 'This core parameter is missing.' };
      return { label: field, value: 'Not provided', status: 'muted', detail: 'Optional in this version.' };
    });

    const preserved = originalPairs.filter(([key]) => !Object.prototype.hasOwnProperty.call(provided, key) && !key.startsWith('utm_'));
    const observations = [
      missing.length ? `Missing core parameters: ${missing.map((field) => field.replace('utm_', '')).join(', ')}.` : 'Source, medium and campaign are present.'
    ];
    if (preserved.length) observations.push(`Preserved ${preserved.length} existing non-UTM query parameter(s).`);
    if (originalPairs.some(([key]) => key.startsWith('utm_'))) observations.push('Existing UTM parameters were preserved unless a new matching value replaced them.');
    if (!providedCount) observations.push('No new parameters were added.');
    if (normalizedFields.length) {
      observations.push(`Normalized to lowercase URL-safe values: ${normalizedFields.join(', ')}.`);
    }
    if (url.hash) observations.push('The original URL fragment remains after rebuilding the query.');

    let recommendation = 'The final URL is ready to copy and use. Validate the naming convention before sharing it.';
    if (!providedCount) recommendation = 'Complete at least source, medium and campaign before using this URL in reporting.';
    else if (missing.length) recommendation = `Complete ${missing[0].replace('utm_', '')} to finish the core tag set.`;
    else if (preserved.length) recommendation = 'The final URL preserves the original query and adds consistent campaign tags. Validate the naming convention before sharing it.';

    const finalUrl = url.toString();
    const html = `
      <section class="tool-result">
        <article class="tool-result__hero tool-result__hero--${overview[1]}">
          <p class="tools-label">Overall status</p><h2>${overview[0]}</h2><p>${overview[2]}</p>
        </article>
        <article class="tool-panel">
          <p class="tools-label">Final URL</p><h3>Built URL</h3>
          <div class="tool-copy-meta"><span class="tool-count-badge">Ready to copy</span><span class="tool-count-badge">5 parameters reviewed</span></div>
          <div class="tool-copy-stack">
            <textarea id="browser-utm-output" class="tool-copy-output tool-copy-output--url" rows="4" readonly>${escapeHtml(finalUrl)}</textarea>
            <div class="tool-copy-row">
              <button type="button" class="button-link" data-browser-copy>Copy URL</button>
              <a class="button-link button-link--dark" href="${escapeHtml(finalUrl)}" target="_blank" rel="noopener noreferrer">Open URL</a>
              <span class="tool-copy-feedback" data-browser-copy-feedback></span>
            </div>
          </div>
        </article>
        <div class="tool-result__grid">
          <article class="tool-panel"><p class="tools-label">Parameters</p><h3>Parameter preview</h3>${renderChecklist(rows)}</article>
          <div class="tool-result__stack">
            <article class="tool-panel tool-panel--soft"><p class="tools-label">Query</p><h3>Preserved parameters</h3>${preserved.length ? `<ul class="tool-inline-list">${preserved.map(([key, value]) => `<li>${escapeHtml(key)}=${escapeHtml(value)}</li>`).join('')}</ul>` : '<p>There were no additional query parameters to preserve.</p>'}</article>
            <article class="tool-panel tool-panel--soft"><p class="tools-label">Observations</p><h3>Tagging review</h3>${renderList(observations, 'No observations.')}</article>
            <article class="tool-panel tool-panel--recommendation"><p class="tools-label">Recommendation</p><h3>Recommended next step</h3><p>${escapeHtml(recommendation)}</p></article>
          </div>
        </div>
      </section>`;

    const target = revealResult(form, html);
    target?.querySelector('[data-browser-copy]')?.addEventListener('click', async (event) => {
      const feedback = target.querySelector('[data-browser-copy-feedback]');
      try {
        await navigator.clipboard.writeText(finalUrl);
        event.currentTarget.textContent = 'Copied';
        if (feedback) feedback.textContent = 'Final URL copied.';
        emitToolEvent(form, 'pi:tool-copy');
      } catch (error) {
        if (feedback) feedback.textContent = 'Copy the URL manually from the field above.';
      }
    });
  }

  function buildCreativeQaResult(form) {
    const data = Object.fromEntries(new FormData(form).entries());
    const rules = FORMAT_RULES[data.format_type];
    const name = String(data.creative_name || '').trim();
    if (!name) throw new Error('Enter a creative name.');
    const dimensions = String(data.dimensions || '').trim().replace(/\s+/g, '').toLowerCase();
    if (dimensions && !/^\d{2,5}x\d{2,5}$/.test(dimensions)) throw new Error('Use a valid dimension format, such as 300x250.');
    const destination = normalizePublicUrl(data.destination_url, false);
    const clickPresent = data.click_tag_present === 'yes';
    const weight = data.weight_kb === '' || data.weight_kb == null ? null : Number(data.weight_kb);
    const items = [
      { label: 'Creative name', status: 'ok', detail: `Declared name: ${name}.` },
      { label: 'Format', status: 'ok', detail: `Declared format: ${rules.label}.` },
      dimensions
        ? { label: 'Dimensions', status: 'ok', detail: `Declared dimensions: ${dimensions}.` }
        : { label: 'Dimensions', status: 'warn', detail: 'No dimensions were declared for this creative.' }
    ];

    if (rules.requiresClick && !clickPresent && !destination) items.push({ label: 'Click path', status: 'fail', detail: 'No click tag or destination URL was supplied for a format that normally needs a click path.' });
    else if (rules.requiresClick && !clickPresent) items.push({ label: 'Click path', status: 'warn', detail: 'A destination URL is present, but the click tag still needs confirmation.' });
    else if (clickPresent && !destination) items.push({ label: 'Click path', status: 'warn', detail: 'A click tag was declared, but no destination URL was supplied for final review.' });
    else if (destination) items.push({ label: 'Click path', status: 'ok', detail: 'A destination URL was declared and is ready for manual review.' });
    else items.push({ label: 'Click path', status: 'muted', detail: 'No destination URL was supplied and this context does not explicitly require a click path.' });

    items.push(data.tracking_urls_included === 'yes'
      ? { label: 'Tracking', status: 'ok', detail: 'Additional tracking URLs were declared for review.' }
      : { label: 'Tracking', status: 'warn', detail: 'No tracking URLs were declared; review measurement before launch.' });

    if (weight == null || Number.isNaN(weight)) items.push({ label: 'Weight', status: 'warn', detail: 'Asset weight was not provided.' });
    else if (weight > rules.maxWeight * 1.5) items.push({ label: 'Weight', status: 'fail', detail: `The declared weight is ${weight} KB, well above the ${rules.maxWeight} KB threshold.` });
    else if (weight > rules.maxWeight) items.push({ label: 'Weight', status: 'warn', detail: `The declared weight is ${weight} KB, above the suggested ${rules.maxWeight} KB threshold.` });
    else items.push({ label: 'Weight', status: 'ok', detail: `The declared weight is within the suggested threshold (${weight} KB of ${rules.maxWeight} KB).` });

    const deviceLabels = { desktop: 'Desktop', mobile: 'Mobile', both: 'Both' };
    items.push({ label: 'Target device', status: 'ok', detail: `Declared device: ${deviceLabels[data.device_target]}.` });
    if (data.autoplay_behavior === 'sound_on') items.push({ label: 'Playback', status: 'fail', detail: 'Autoplay with sound was declared and should be corrected before approval.' });
    else if (data.sound_behavior === 'load') items.push({ label: 'Playback', status: 'fail', detail: 'Sound starts on load; block the creative until this behavior is corrected.' });
    else if (data.autoplay_behavior === 'muted') items.push({ label: 'Playback', status: 'warn', detail: 'Muted autoplay was declared; validate placement policy and expected behavior.' });
    else if (data.sound_behavior === 'user_action') items.push({ label: 'Playback', status: 'ok', detail: 'Sound is tied to a user interaction.' });
    else items.push({ label: 'Playback', status: 'ok', detail: 'Declared behavior: no autoplay and no sound.' });

    items.push(data.serving_context === 'unknown'
      ? { label: 'Serving context', status: 'warn', detail: 'The serving context is undefined; confirm SafeFrame or friendly iframe behavior.' }
      : { label: 'Serving context', status: 'ok', detail: `Declared context: ${data.serving_context === 'safeframe' ? 'SafeFrame' : 'Friendly iframe'}.` });
    items.push(String(data.extra_notes || '').trim()
      ? { label: 'Notes', status: 'ok', detail: 'Operational notes were added for the review.' }
      : { label: 'Notes', status: 'muted', detail: 'No additional notes were supplied in this run.' });

    const passed = items.filter((item) => item.status === 'ok').map((item) => item.detail);
    const observations = items.filter((item) => item.status === 'warn').map((item) => item.detail);
    const flags = items.filter((item) => item.status === 'fail').map((item) => item.detail);
    const state = flags.length ? 'Blocked' : observations.length ? 'Review needed' : 'Ready';
    const tone = flags.length ? 'critical' : observations.length ? 'warn' : 'good';
    const summary = flags.length
      ? `${name} has ${flags.length} blocker(s) and ${observations.length} caution(s). Correct critical items before approval.`
      : observations.length
        ? `${name} has no direct blockers, but ${observations.length} item(s) need review before launch.`
        : `${name} passes this initial rule-based review without strong warnings.`;
    const recommendation = flags.length
      ? `Immediate priority: resolve ${flags[0].toLowerCase()} Then run the checklist again.`
      : observations.length
        ? `Review ${observations[0].toLowerCase()} Keep this output as a documented preflight checklist.`
        : 'The creative is ready for final operational review or trafficking.';

    revealResult(form, `
      <section class="tool-result">
        <article class="tool-result__hero tool-result__hero--${tone}"><p class="tools-label">Final status</p><h2>${state}</h2><p>${escapeHtml(summary)}</p></article>
        <article class="tool-panel"><p class="tools-label">Summary</p><h3>Checklist summary</h3>
          <div class="tool-metric-grid tool-metric-grid--triple">
            <div class="tool-metric"><span>Passed checks</span><strong>${passed.length}</strong></div>
            <div class="tool-metric"><span>Observations</span><strong>${observations.length}</strong></div>
            <div class="tool-metric"><span>Flags</span><strong>${flags.length}</strong></div>
          </div>
        </article>
        <div class="tool-result__grid">
          <article class="tool-panel"><p class="tools-label">Checklist</p><h3>Structured review</h3>${renderChecklist(items)}</article>
          <article class="tool-panel"><p class="tools-label">Passed checks</p><h3>Passed checks</h3>${renderList(passed, 'No clear passed checks were recorded.')}</article>
          <article class="tool-panel"><p class="tools-label">Observations</p><h3>Observations</h3>${renderList(observations, 'No observations were recorded.')}</article>
          <article class="tool-panel"><p class="tools-label">Flags</p><h3>Review flags</h3>${renderList(flags, 'No strong flags were recorded.')}</article>
        </div>
        <article class="tool-panel"><p class="tools-label">Recommendation</p><h3>Recommended next step</h3><p>${escapeHtml(recommendation)}</p></article>
      </section>`);
  }

  function analyzePreviewMarkup(code) {
    const documentNode = new DOMParser().parseFromString(code || '', 'text/html');
    const scripts = Array.from(documentNode.querySelectorAll('script'));
    const iframes = Array.from(documentNode.querySelectorAll('iframe'));
    const links = Array.from(documentNode.querySelectorAll('a'));
    const media = Array.from(documentNode.querySelectorAll('video, audio'));
    const references = Array.from(documentNode.querySelectorAll('[src], [href]'))
      .map((node) => node.getAttribute('src') || node.getAttribute('href') || '')
      .filter((value) => /^(https?:)?\/\//i.test(value));
    const inlineHandlers = Array.from(documentNode.querySelectorAll('*')).reduce((count, node) => (
      count + Array.from(node.attributes).filter((attribute) => attribute.name.toLowerCase().startsWith('on')).length
    ), 0);
    return {
      scripts,
      iframes,
      links,
      media,
      references: Array.from(new Set(references)),
      autoplay: media.filter((node) => node.hasAttribute('autoplay')).length,
      audio: documentNode.querySelectorAll('audio').length,
      inlineHandlers
    };
  }

  function buildCreativePreviewResult(form) {
    const data = Object.fromEntries(new FormData(form).entries());
    const width = Number(data.width);
    const height = Number(data.height);
    if (!Number.isInteger(width) || width < 1 || width > 4000 || !Number.isInteger(height) || height < 1 || height > 4000) {
      throw new Error('Width and height must be between 1 and 4000 pixels.');
    }
    const clickUrl = normalizePublicUrl(data.click_url, false);
    const code = String(data.code || '').trim();
    const analysis = analyzePreviewMarkup(code);
    const macroMatches = code.match(/%%[A-Z0-9_]+%%|\{\{[^}]+\}\}|\$\{[^}]+\}|\[\[?[A-Z0-9_]+\]?\]|\bclicktag\b/gi) || [];
    const placeholderMatches = code.match(/replace[_ -]?me|\btodo\b|example\.com|your[-_ ]?click[-_ ]?url/gi) || [];
    const blocked = /top\.location|parent\.location|window\.top|window\.parent|document\.location/i.test(code);
    const partial = data.input_mode === 'third_party' || analysis.scripts.length || analysis.iframes.length || analysis.references.length || macroMatches.length;
    const label = !code ? 'No content' : blocked ? 'Blocked' : partial ? 'Partial' : 'Rendered';
    const tone = label === 'Rendered' ? 'good' : label === 'Blocked' ? 'critical' : 'warn';
    const summary = !code
      ? 'No code was supplied. There is no preview or technical reading yet.'
      : blocked
        ? 'The preview did not run because the code includes frame-navigation patterns that are unsafe in this sandbox.'
        : partial
          ? 'The creative includes executable code, external references or unresolved macros, so the preview may remain partial.'
          : 'The preview rendered in the sandbox without an obvious external execution dependency.';

    const flags = [];
    if (!code) flags.push('No code was supplied for review.');
    if (blocked) flags.push('The visual preview was blocked because of frame-navigation or container-escape patterns.');
    if (analysis.autoplay) flags.push('Media tags with autoplay were detected; review the placement policy.');
    if (analysis.audio && analysis.autoplay) flags.push('Audio or video autoplay needs technical review before approval.');
    if (!analysis.links.length && !clickUrl && ['display', 'rich_media'].includes(data.creative_type)) flags.push('No links or reference click URL were found for a format that likely needs a click path.');
    if (data.input_mode === 'third_party' && !analysis.scripts.length && !analysis.iframes.length) flags.push('Third-party tag mode was selected, but the supplied code contains no scripts or iframes.');
    if (placeholderMatches.length) flags.push('The code contains visible placeholders or incomplete text.');

    const observations = [];
    if (!code) observations.push('Paste a creative or tag to generate a preview and findings.');
    if (analysis.scripts.length) observations.push('The creative includes scripts; execution may depend on external resources or environment conditions.');
    if (analysis.iframes.length) observations.push('Iframes were detected; part of the content may live outside the primary sandbox.');
    if (analysis.references.length) observations.push('External references may render partially or be blocked by availability or resource policy.');
    if (macroMatches.length) observations.push('Visible macros or placeholders are not replaced automatically by this preview.');
    if (clickUrl && !analysis.links.length) observations.push('A click URL was declared, but this version does not inject it into the markup.');
    if (analysis.inlineHandlers) observations.push('Inline handlers were detected; review their behavior and JavaScript dependencies.');
    if (analysis.media.length && !analysis.autoplay) observations.push('Media tags have no visible autoplay. Codecs, weight and placement policies still need review.');
    if (String(data.notes || '').trim()) observations.push('Operational notes provide context for the review.');
    if (label === 'Partial') observations.push('Treat this as a constrained sandbox, not an exact reproduction of the serving environment.');
    if (!observations.length) observations.push('No additional observations appeared in this run.');

    const limitations = [
      'The preview runs in a sandboxed iframe and prioritizes stability over absolute fidelity.',
      'It does not simulate a real ad server, SafeFrame, network tracking or full placement compatibility.'
    ];
    if (data.input_mode === 'third_party' || analysis.scripts.length || analysis.iframes.length) limitations.push('Third-party execution can depend on external environments and render partially.');
    if (blocked) limitations.push('This version prevents frame-navigation or escape patterns.');
    if (analysis.references.length) limitations.push('External scripts or resources may fail, be delayed or render partially in the sandbox.');

    let recommendation = ['Ready for initial review', 'The creative is ready for an initial visual and technical review in this constrained sandbox.'];
    if (!code) recommendation = ['No content', 'Paste code and render again to generate a preview and first-pass findings.'];
    else if (blocked) recommendation = ['Cannot be fully validated', 'Visual execution is unsafe in this sandbox. Use a more controlled technical review.'];
    else if (flags.length) recommendation = [label === 'Rendered' ? 'Technical review needed' : 'Partial preview', `First priority: ${flags[0].toLowerCase()} Then repeat the preview.`];
    else if (partial) recommendation = ['Partial preview', 'The preview is useful for an initial reading, but final behavior may depend on external environments.'];

    const detected = [
      ['Scripts', analysis.scripts.length, analysis.scripts.length ? `${analysis.scripts.length} script tag(s) detected.` : 'No script tags were detected.'],
      ['Iframes', analysis.iframes.length, analysis.iframes.length ? `${analysis.iframes.length} iframe(s) detected.` : 'No iframes were detected.'],
      ['Links', analysis.links.length, analysis.links.length ? `${analysis.links.length} link(s) detected.` : 'No links were detected.'],
      ['External resources', analysis.references.length, analysis.references.length ? `${analysis.references.length} external reference(s) detected.` : 'No external references were detected.'],
      ['Media tags', analysis.media.length, analysis.media.length ? `${analysis.media.length} media tag(s) detected.` : 'No media tags were detected.'],
      ['Macros / placeholders', new Set([...macroMatches, ...placeholderMatches]).size, macroMatches.length || placeholderMatches.length ? 'Macros or visible placeholders require review.' : 'No macros or visible placeholders were detected.']
    ];

    const target = revealResult(form, `
      <section class="tool-result">
        <article class="tool-result__hero tool-result__hero--${tone}"><p class="tools-label">Preview status</p><h2>${label}</h2><p>${escapeHtml(summary)}</p></article>
        <article class="tool-panel">
          <p class="tools-label">Preview</p><h3>Isolated preview area</h3>
          <div class="tool-preview-shell">
            <div class="tool-preview-meta"><span>${width} x ${height} px</span><span>${escapeHtml(INPUT_LABELS[data.input_mode])}</span><span>${escapeHtml(TYPE_LABELS[data.creative_type])}</span></div>
            <div class="tool-preview-stage" data-browser-preview-stage></div>
            <p class="tool-panel__note">Sandboxed preview only. It does not reproduce SafeFrame, an ad server, network validation or a real click path.</p>
          </div>
        </article>
        <div class="tool-result__grid">
          <article class="tool-panel"><p class="tools-label">Detected elements</p><h3>Detected elements</h3><div class="tool-detected-grid">${detected.map(([itemLabel, count, detail]) => `<article class="tool-detected-item"><div class="tool-detected-item__top"><strong>${escapeHtml(itemLabel)}</strong><span class="tool-count-badge">${count}</span></div><p>${escapeHtml(detail)}</p></article>`).join('')}</div></article>
          <article class="tool-panel"><p class="tools-label">Technical observations</p><h3>Observations and flags</h3>${renderList([...flags, ...observations], 'No observations.')}</article>
          <article class="tool-panel"><p class="tools-label">Limitations</p><h3>Preview limitations</h3>${renderList(limitations, 'No limitations.')}</article>
        </div>
        <article class="tool-panel"><p class="tools-label">Recommendation</p><h3>${escapeHtml(recommendation[0])}</h3><p>${escapeHtml(recommendation[1])}</p></article>
      </section>`);

    const stage = target?.querySelector('[data-browser-preview-stage]');
    if (!stage) return;
    if (!code) {
      stage.innerHTML = '<div class="tool-preview-placeholder"><strong>Preview area</strong><span>Paste code and render it to inspect the constrained sandbox.</span></div>';
      return;
    }
    const iframe = document.createElement('iframe');
    iframe.className = 'tool-preview-frame';
    iframe.title = 'Creative preview';
    iframe.width = String(width);
    iframe.height = String(height);
    iframe.setAttribute('sandbox', 'allow-scripts allow-forms');
    iframe.referrerPolicy = 'no-referrer';
    iframe.srcdoc = blocked
      ? '<!doctype html><html><body style="margin:0;background:#090d13;color:#fff;font:16px system-ui;display:grid;place-items:center;min-height:100vh"><div style="padding:24px"><strong>Preview blocked in the sandbox</strong><p>Frame-navigation patterns were detected.</p></div></body></html>'
      : (/<!doctype|<html[\s>]/i.test(code) ? code : `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;padding:0;width:100%;height:100%;background:#090d13;overflow:auto}*{box-sizing:border-box}.preview-root{width:${width}px;min-height:${height}px;pointer-events:none}</style></head><body><div class="preview-root">${code}</div></body></html>`);
    stage.appendChild(iframe);
  }

  const handlers = {
    'utm-builder': buildUtmResult,
    'creative-qa-checklist': buildCreativeQaResult,
    'creative-preview-lab': buildCreativePreviewResult
  };

  function initBrowserTools() {
    document.querySelectorAll('form[data-browser-tool]').forEach((form) => {
      form.querySelectorAll('[data-utm-preset]').forEach((button) => {
        button.addEventListener('click', () => applyUtmPreset(form, button.dataset.utmPreset));
      });
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        if (event.submitter?.name === '_use_example') loadExample(form);
        if (!form.reportValidity()) {
          emitToolEvent(form, 'pi:tool-error', { error_type: 'required_field' });
          return;
        }
        try {
          const handler = handlers[form.dataset.browserTool];
          if (!handler) throw new Error('This tool is not available.');
          handler(form);
          emitToolEvent(form, 'pi:tool-complete');
        } catch (error) {
          showError(form, error instanceof Error ? error.message : 'Check the entered information and try again.');
          emitToolEvent(form, 'pi:tool-error', { error_type: 'invalid_input' });
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', initBrowserTools);
}());
