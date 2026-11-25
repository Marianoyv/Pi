/* First-party GA4 boundary: analytics enabled by default, safe parameters and preview isolation. */
(() => {
  'use strict';
  const script = document.currentScript;
  const id = script?.dataset.measurementId || '';
  if (!/^G-[A-Z0-9]+$/.test(id)) return;
  const production = new URL(script.dataset.productionOrigin);
  const allowedHosts = new Set([production.hostname, ...(script.dataset.productionHosts || "").split(",").map(host => host.trim()).filter(Boolean)]);
  const local = location.protocol !== "https:" || !allowedHosts.has(location.hostname);
  const debug = new URLSearchParams(location.search).get('analytics_debug') === '1';
  const available = !local || debug;
  const collect = !local;
  const consentKey = 'pi-analytics-consent-v1';
  const denied = { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
  const analyticsGranted = { ...denied, analytics_storage: 'granted' };
  const events = new Set(['contact_cta_click', 'contact_start', 'tool_use', 'tool_error', 'tool_result_copy', 'outbound_click', 'project_preview_open', 'utm_preset_select', 'editorial_article_view', 'editorial_read_progress', 'editorial_engaged_time', 'editorial_to_pi', 'section_view', 'page_read_progress', 'page_engaged_time', 'plan_view', 'plan_select', 'navigation_click', 'case_study_open', 'product_open', 'section_jump', 'web_vital', 'video_start', 'video_progress', 'video_complete', 'control_click', 'form_start', 'form_submit', 'form_error', 'file_download', 'details_open']);
  const fields = new Set(['contact_method', 'link_location', 'link_text', 'tool_name', 'error_type', 'link_domain', 'project_name', 'preset_name', 'article_slug', 'article_type', 'article_cluster', 'returning_reader', 'read_percent', 'milestone_seconds', 'destination_section', 'origin_article_slug', 'origin_article_cluster', 'section_id', 'plan_name', 'case_name', 'metric_name', 'metric_value', 'metric_delta', 'metric_rating', 'metric_id', 'navigation_type', 'video_title', 'video_percent', 'video_provider', 'control_name', 'control_location', 'form_name', 'file_name', 'file_extension', 'details_id']);
  let consent = 'unknown';
  let configured = false;
  let tagLoaded = false;
  const preferences = document.querySelector('[data-analytics-preferences]');
  const settingsButtons = document.querySelectorAll('[data-analytics-settings]');
  const vitalsURL = new URL('./vendor/web-vitals.js', script.src).href;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  function safeText(value) {
    if (typeof value !== 'string') return '';
    const text = value.trim().slice(0, 100);
    if (/@|mailto:|tel:|https?:\/\/|(?:\+?\d[\s().-]*){7,}/i.test(text)) return '';
    return text;
  }
  function safePath(path) {
    try { path = decodeURIComponent(path); } catch (_) { return '/'; }
    if (!safeText(path) && path !== '/') return '/';
    return path.slice(0, 100);
  }
  const path = safePath(location.pathname);
  let referrer = '';
  try {
    const previous = new URL(document.referrer);
    referrer = previous.origin + (previous.origin === location.origin ? safePath(previous.pathname) : '/');
  } catch (_) { /* A direct visit has no referrer. */ }
  const context = { page_path: path, page_type: script.dataset.pageType || 'page', content_language: document.documentElement.lang || 'en' };
  const page = { page_location: location.origin + path, page_referrer: referrer, page_title: safeText(document.title) || 'Pi Development' };

  function enabled() { return available && consent === 'granted'; }
  function measuring() { return available && configured && consent !== 'disabled'; }
  function track(name, parameters = {}) {
    if (!measuring() || !events.has(name)) return false;
    const clean = {};
    Object.entries(parameters).forEach(([key, value]) => {
      if (!fields.has(key)) return;
      if (typeof value === 'number' && Number.isFinite(value)) clean[key] = value;
      else if (key === 'metric_id' && /^[a-z0-9-]{1,100}$/i.test(String(value))) clean[key] = value;
      else {
        const text = safeText(value);
        if (text) clean[key] = text;
      }
    });
    window.gtag('event', name, { ...clean, ...context, transport_type: 'beacon' });
    return true;
  }
  function readChoice() {
    try {
      const stored = JSON.parse(localStorage.getItem(consentKey) || 'null');
      if (stored?.version === 1 && ['granted', 'denied', 'disabled'].includes(stored.choice) && Date.now() - stored.savedAt < 180 * 86400000) return stored.choice;
    } catch (_) { /* Consent can still be chosen without persistent storage. */ }
    return 'unknown';
  }
  function clearMeasurementStorage() {
    try {
      localStorage.removeItem('pi-editorial-origin-v1');
      localStorage.removeItem('pi-editorial-reader-v1');
    } catch (_) { /* Storage may be unavailable. */ }
    const domains = location.hostname.split('.');
    document.cookie.split(';').map(item => item.split('=')[0].trim()).filter(name => /^_ga(?:_|$)/.test(name)).forEach(name => {
      document.cookie = name + '=; Max-Age=0; path=/';
      for (let i = 0; i < domains.length - 1; i += 1) {
        document.cookie = name + '=; Max-Age=0; path=/; domain=.' + domains.slice(i).join('.');
      }
    });
  }
  function start() {
    if (configured || consent === 'disabled') return;
    configured = true;
    const campaign = {};
    const query = new URLSearchParams(location.search);
    const mapping = { source: 'source', medium: 'medium', campaign: 'name', id: 'id', content: 'content', term: 'term' };
    Object.entries(mapping).forEach(([utm, field]) => {
      const value = safeText(query.get('utm_' + utm) || '');
      if (value) campaign['campaign_' + field] = value;
    });
    window.gtag('set', { ...page, ...context });
    window.gtag('js', new Date());
    window.gtag('config', id, { ...page, ...campaign, send_page_view: false, allow_google_signals: false, allow_ad_personalization_signals: false, ...(debug ? { debug_mode: true } : {}) });
    window.gtag('event', 'page_view', { ...page, ...context });
    if (collect && !tagLoaded) {
      tagLoaded = true;
      const tag = document.createElement('script');
      tag.async = true;
      tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
      document.head.append(tag);
    }
  }
  function setConsent(choice, persist = true) {
    if (!available || !['granted', 'denied', 'disabled'].includes(choice)) return;
    const wasEnabled = enabled();
    consent = choice;
    if (persist) {
      try { localStorage.setItem(consentKey, JSON.stringify({ choice, version: 1, savedAt: Date.now() })); } catch (_) { /* Optional storage. */ }
    }
    window.gtag('consent', 'update', { ...denied, analytics_storage: choice === 'granted' ? 'granted' : 'denied' });
    if (preferences) preferences.hidden = true;
    window['ga-disable-' + id] = choice === 'disabled';
    if (choice !== 'disabled') start();
    if (choice === 'granted') {
      if (!wasEnabled) window.dispatchEvent(new CustomEvent('pi:analyticsready'));
    } else clearMeasurementStorage();
  }
  window.PiAnalytics = { track, isEnabled: enabled, isMeasuring: measuring, setConsent, debug, collect, openSettings() { if (available && preferences) preferences.hidden = false; } };
  if (!available) return;
  window.gtag('consent', 'default', analyticsGranted);
  settingsButtons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => window.PiAnalytics.openSettings());
  });
  document.querySelectorAll('[data-analytics-consent]').forEach(button => button.addEventListener('click', () => setConsent(button.dataset.analyticsConsent)));
  const stored = readChoice();
  if (stored === 'unknown') {
    consent = 'granted';
    start();
  } else setConsent(stored, false);

  let observersStarted = false;
  function observePage() {
    if (observersStarted) return;
    observersStarted = true;
    const seen = new WeakSet();
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {
        if (!measuring() || !entry.isIntersecting || seen.has(entry.target)) return;
        if (entry.intersectionRect.height < Math.min(100, entry.target.offsetHeight * .3)) return;
        seen.add(entry.target);
        const plan = entry.target.dataset.plan;
        track(plan ? 'plan_view' : 'section_view', plan ? { plan_name: plan } : { section_id: entry.target.getAttribute('aria-labelledby') || entry.target.id });
      }), { threshold: [0, .1, .25, .5, .75, 1] });
      document.querySelectorAll('main > section[aria-labelledby], [data-plan]').forEach(section => observer.observe(section));
    }
    if (context.page_type !== 'knowledge_page') {
      const reached = new Set();
      const depth = () => {
        if (!measuring()) return;
        const height = document.documentElement.scrollHeight - innerHeight;
        if (height <= 0) return;
        const percent = Math.min(100, scrollY / height * 100);
        [25, 50, 75, 90].forEach(value => {
          if (percent >= value && !reached.has(value)) { reached.add(value); track('page_read_progress', { read_percent: value }); }
        });
      };
      window.addEventListener('scroll', depth, { passive: true });
      let seconds = 0;
      window.setInterval(() => {
        if (!measuring() || document.visibilityState !== 'visible' || !document.hasFocus()) return;
        seconds += 5;
        if ([30, 60, 120, 300].includes(seconds)) track('page_engaged_time', { milestone_seconds: seconds });
      }, 5000);
    }
    document.addEventListener('click', event => {
      const link = event.target.closest('a[href]');
      const control = event.target.closest('button, [role="button"]');
      if (control && measuring() && !control.matches('[data-analytics-consent], [data-analytics-settings]')) {
        const controlLocation = control.closest('nav') ? 'navigation' : control.closest('footer') ? 'footer' : control.closest('form') ? 'form' : 'content';
        track('control_click', {
          control_name: control.dataset.analyticsLabel || control.getAttribute('aria-label') || control.textContent || 'button',
          control_location: controlLocation
        });
      }
      if (!link || !measuring()) return;
      const destination = new URL(link.href, location.href);
      const plan = link.closest('[data-plan]')?.dataset.plan;
      if (plan) track('plan_select', { plan_name: plan, link_location: 'plan_card' });
      if (link.closest('nav')) track('navigation_click', { destination_section: safePath(destination.pathname), link_location: 'navigation' });
      if (destination.origin !== location.origin) return;
      if (/^\/work\/[^/]+\/$/.test(destination.pathname)) track('case_study_open', { case_name: destination.pathname.split('/')[2] });
      if (/^\/products\/[^/]+\/$/.test(destination.pathname)) track('product_open', { tool_name: destination.pathname.split('/')[2] });
      if (destination.pathname === location.pathname && destination.hash) track('section_jump', { section_id: destination.hash.slice(1) });
      const download = destination.pathname.match(/\/([^/]+)\.([a-z0-9]{1,8})$/i);
      if (download && (link.hasAttribute('download') || /^(pdf|csv|json|zip|docx?|xlsx?|pptx?)$/i.test(download[2]))) {
        track('file_download', { file_name: download[1], file_extension: download[2].toLowerCase(), link_location: link.closest('footer') ? 'footer' : 'content' });
      }
    });
    const startedForms = new WeakSet();
    document.addEventListener('focusin', event => {
      const form = event.target.closest('form');
      if (!form || startedForms.has(form) || !measuring()) return;
      startedForms.add(form);
      track('form_start', { form_name: form.dataset.analyticsName || form.getAttribute('name') || form.id || 'form' });
    });
    document.addEventListener('submit', event => {
      const form = event.target.closest('form');
      if (!form || !measuring()) return;
      track('form_submit', { form_name: form.dataset.analyticsName || form.getAttribute('name') || form.id || 'form' });
    });
    document.addEventListener('invalid', event => {
      const form = event.target.closest('form');
      if (!form || !measuring()) return;
      track('form_error', {
        form_name: form.dataset.analyticsName || form.getAttribute('name') || form.id || 'form',
        error_type: event.target.getAttribute('type') || 'invalid_field'
      });
    }, true);
    document.addEventListener('toggle', event => {
      const details = event.target.closest('details');
      if (!details?.open || !measuring()) return;
      track('details_open', { details_id: details.id || details.querySelector('summary')?.textContent || 'details' });
    }, true);
    document.querySelectorAll('video:not([autoplay])').forEach(video => {
      if (video.closest('[aria-hidden="true"]')) return;
      const videoTitle = video.dataset.analyticsTitle || 'project_video';
      const reported = new Set();
      const report = (name, percent) => {
        const key = name + percent;
        if (!measuring() || reported.has(key)) return;
        reported.add(key);
        track(name, { video_title: videoTitle, video_provider: 'html5', video_percent: percent });
      };
      video.addEventListener('play', () => report('video_start', 0));
      video.addEventListener('timeupdate', () => {
        if (!video.duration) return;
        [10, 25, 50, 75].forEach(percent => { if (video.currentTime / video.duration * 100 >= percent) report('video_progress', percent); });
      });
      video.addEventListener('ended', () => report('video_complete', 100));
    });
    if ('PerformanceObserver' in window) {
      import(vitalsURL).then(vitals => {
        const report = metric => track('web_vital', {
          metric_name: metric.name, metric_value: Math.round(metric.value * (metric.name === 'CLS' ? 1000 : 1)),
          metric_delta: Math.round(metric.delta * (metric.name === 'CLS' ? 1000 : 1)), metric_rating: metric.rating,
          metric_id: metric.id, navigation_type: metric.navigationType
        });
        [vitals.onLCP, vitals.onINP, vitals.onCLS, vitals.onFCP, vitals.onTTFB].forEach(register => register(report));
      }).catch(() => { /* Measurement must never interrupt site interactions. */ });
    }
  }
  window.addEventListener('pi:analyticsready', observePage);
  if (measuring()) observePage();
})();
