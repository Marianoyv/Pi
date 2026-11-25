const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('static/web/js/analytics.js', 'utf8');

function browser({ origin = 'https://pidevelopment.web.app', query = '', stored = null, storageFails = false } = {}) {
  const listeners = new Map();
  const tagRequests = [];
  const cookieWrites = [];
  const storage = new Map(stored ? [['pi-analytics-consent-v1', JSON.stringify(stored)]] : []);
  const preferences = { hidden: true };
  const settings = { hidden: true, addEventListener() {} };
  const location = new URL('/planes-web/' + query, origin);
  const document = {
    currentScript: { src: origin + '/static/web/js/analytics.js', dataset: { measurementId: 'G-6XVTWEY4LW', productionOrigin: 'https://pidevelopment.web.app', productionHosts: 'pidevelopment.web.app,pidevelopment.firebaseapp.com', pageType: 'web_plans' } },
    referrer: 'https://search.example/private/person@example.com?email=person@example.com',
    title: 'Website plans | Pi Development', documentElement: { lang: 'en', scrollHeight: 3000 },
    visibilityState: 'visible', hasFocus: () => true,
    querySelector: selector => selector === '[data-analytics-preferences]' ? preferences : null,
    querySelectorAll: selector => selector === '[data-analytics-settings]' ? [settings] : [],
    createElement: () => ({}), head: { append: element => tagRequests.push(element) }, addEventListener() {}
  };
  Object.defineProperty(document, 'cookie', { get: () => '_ga=123; _ga_EXAMPLE=456; session=keep', set: value => cookieWrites.push(value) });
  const localStorage = {
    getItem(key) { if (storageFails) throw Error('blocked'); return storage.get(key) || null; },
    setItem(key, value) { if (storageFails) throw Error('blocked'); storage.set(key, value); },
    removeItem(key) { if (storageFails) throw Error('blocked'); storage.delete(key); }
  };
  const window = {
    addEventListener(name, callback) { const handlers = listeners.get(name) || []; handlers.push(callback); listeners.set(name, handlers); },
    dispatchEvent(event) { (listeners.get(event.type) || []).forEach(callback => callback(event)); }, setInterval: () => 1
  };
  vm.runInNewContext(source, { window, document, location, localStorage, URL, URLSearchParams, innerHeight: 800, scrollY: 0, CustomEvent: class { constructor(type) { this.type = type; } } });
  const calls = () => (window.dataLayer || []).map(args => Array.from(args));
  return { api: window.PiAnalytics, calls, tagRequests, cookieWrites, storage, preferences, settings };
}
const eventCalls = env => env.calls().filter(call => call[0] === 'event');

test('new production visitor starts full analytics without showing a banner', () => {
  const env = browser();
  assert.equal(env.preferences.hidden, true);
  assert.equal(env.api.isEnabled(), true);
  assert.equal(env.api.isMeasuring(), true);
  assert.equal(env.tagRequests.length, 1);
  assert.equal(eventCalls(env).filter(call => call[1] === 'page_view').length, 1);
  assert.equal(env.api.track('contact_start', { contact_method: 'email' }), true);
  assert.equal(env.calls()[0][1], 'default');
  assert.equal(env.calls()[0][2].analytics_storage, 'granted');
  assert.equal(env.calls()[0][2].ad_storage, 'denied');
  assert.equal(env.calls()[0][2].ad_user_data, 'denied');
  assert.equal(env.calls()[0][2].ad_personalization, 'denied');
});
test('grant loads one tag and one page view, despite repeated grant', () => {
  const env = browser();
  env.api.setConsent('granted');
  env.api.setConsent('granted');
  assert.equal(env.tagRequests.length, 1);
  assert.equal(eventCalls(env).filter(call => call[1] === 'page_view').length, 1);
  assert.equal(env.calls().find(call => call[0] === 'config')[2].send_page_view, false);
  assert.equal(env.calls().find(call => call[0] === 'config')[2].allow_google_signals, false);
});
test('revoking storage keeps cookieless events and clears only measurement storage', () => {
  const env = browser();
  env.api.setConsent('granted');
  env.storage.set('pi-editorial-origin-v1', 'private');
  env.storage.set('pi-editorial-reader-v1', 'seen');
  env.api.setConsent('denied');
  const previous = eventCalls(env).length;
  assert.equal(env.api.track('tool_use', { tool_name: 'utm-builder' }), true);
  assert.equal(eventCalls(env).length, previous + 1);
  assert.equal(env.storage.has('pi-editorial-origin-v1'), false);
  assert.ok(env.cookieWrites.some(value => value.startsWith('_ga=;')));
  assert.ok(env.cookieWrites.every(value => !value.startsWith('session=')));
});
test('full opt-out persists, prevents tag loading and stops future events', () => {
  const saved = browser({ stored: { choice: 'disabled', version: 1, savedAt: Date.now() } });
  assert.equal(saved.api.isEnabled(), false);
  assert.equal(saved.api.isMeasuring(), false);
  assert.equal(saved.tagRequests.length, 0);
  assert.equal(saved.api.track('tool_use', { tool_name: 'utm-builder' }), false);

  const active = browser();
  active.api.setConsent('disabled');
  const previous = eventCalls(active).length;
  assert.equal(active.api.track('tool_use', { tool_name: 'utm-builder' }), false);
  assert.equal(eventCalls(active).length, previous);
  assert.equal(JSON.parse(active.storage.get('pi-analytics-consent-v1')).choice, 'disabled');
});
test('local development never loads Google, including dry-run debugging', () => {
  const local = browser({ origin: 'http://127.0.0.1:8000' });
  local.api.setConsent('granted');
  assert.equal(local.api.isEnabled(), false);
  assert.equal(local.tagRequests.length, 0);
  const debug = browser({ origin: 'http://127.0.0.1:8000', query: '?analytics_debug=1' });
  debug.api.setConsent('granted');
  assert.equal(debug.api.track('tool_use', { tool_name: 'utm-builder' }), true);
  assert.equal(debug.tagRequests.length, 0);
  assert.equal(debug.api.collect, false);
});
test('PII, complete URLs and arbitrary parameters are excluded', () => {
  const env = browser({ query: '?email=person@example.com#private' });
  env.api.setConsent('granted');
  env.api.track('contact_start', { contact_method: 'email', link_text: 'person@example.com', form_contents: 'private', link_domain: 'example.com', unknown_url: 'https://example.com/private', page_path: '/override' });
  const params = eventCalls(env).find(call => call[1] === 'contact_start')[2];
  assert.equal(params.link_text, undefined);
  assert.equal(params.form_contents, undefined);
  assert.equal(params.unknown_url, undefined);
  assert.equal(params.page_path, '/planes-web/');
  const page = eventCalls(env).find(call => call[1] === 'page_view')[2];
  assert.equal(page.page_location, 'https://pidevelopment.web.app/planes-web/');
  assert.equal(page.page_referrer, 'https://search.example/');
});
test('safe campaign attribution survives URL cleanup; unsafe fields do not', () => {
  const env = browser({ query: '?utm_source=linkedin&utm_medium=social&utm_campaign=person%40example.com' });
  env.api.setConsent('granted');
  const config = env.calls().find(call => call[0] === 'config')[2];
  assert.equal(config.campaign_source, 'linkedin');
  assert.equal(config.campaign_medium, 'social');
  assert.equal(config.campaign_name, undefined);
});
test('saved consent works, expired consent falls back to full analytics, blocked storage is supported', () => {
  const saved = browser({ stored: { choice: 'granted', version: 1, savedAt: Date.now() } });
  assert.equal(saved.api.isEnabled(), true);
  assert.equal(saved.tagRequests.length, 1);
  const expired = browser({ stored: { choice: 'granted', version: 1, savedAt: Date.now() - 181 * 86400000 } });
  assert.equal(expired.api.isEnabled(), true);
  assert.equal(expired.api.isMeasuring(), true);
  assert.equal(expired.preferences.hidden, true);
  const blocked = browser({ storageFails: true });
  blocked.api.setConsent('granted');
  assert.equal(blocked.api.isEnabled(), true);
});
test('contact intent is measured without inventing confirmed leads or purchases', () => {
  const env = browser();
  env.api.setConsent('granted');
  assert.equal(env.api.track('contact_start', { contact_method: 'whatsapp', plan_name: 'catalogo' }), true);
  assert.equal(env.api.track('generate_lead', { value: 1000 }), false);
  assert.equal(env.api.track('purchase', { value: 1000 }), false);
});
