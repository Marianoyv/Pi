const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

const source = readFileSync('static/web/js/contact-brief.js', 'utf8');

function loadApi() {
  const window = {};
  const document = { querySelectorAll: () => [] };
  vm.runInNewContext(source, { window, document, URL, FormData: class {} });
  return window.PiContactBrief;
}

test('builds a concise project brief and normalizes user spacing', () => {
  const api = loadApi();
  const brief = api.buildBrief({
    project_type: '  Product or MVP ',
    current_stage: 'Exploring   an idea',
    outcome: 'Orders arrive in several places.\n\n We need one reliable flow. ',
    timeline: 'Within 1–3 months'
  });

  assert.match(brief, /^Hello Mariano,/);
  assert.match(brief, /Project type: Product or MVP/);
  assert.match(brief, /Current stage: Exploring an idea/);
  assert.match(brief, /Orders arrive in several places\.\nWe need one reliable flow\./);
  assert.match(brief, /Timing: Within 1–3 months$/);
});

test('encodes the complete brief in WhatsApp and email links', () => {
  const api = loadApi();
  const brief = api.buildBrief({
    project_type: 'Internal tool or automation',
    current_stage: 'Replacing a manual workflow',
    outcome: 'Reduce duplicate work & avoid errors <script>alert(1)</script>.',
    timeline: 'As soon as practical'
  });
  const links = api.buildLinks(brief, 'https://wa.me/5491170619703', 'pidev.founder@gmail.com');
  const whatsapp = new URL(links.whatsapp);
  const email = new URL(links.email);

  assert.equal(whatsapp.origin, 'https://wa.me');
  assert.equal(whatsapp.searchParams.get('text'), brief);
  assert.equal(email.protocol, 'mailto:');
  assert.equal(email.searchParams.get('subject'), 'Project inquiry | Pi Development');
  assert.equal(email.searchParams.get('body'), brief);
  assert.match(brief, /<script>alert\(1\)<\/script>/);
});

test('contact brief runtime does not send data over the network', () => {
  assert.equal(source.includes('fetch('), false);
  assert.equal(source.includes('XMLHttpRequest'), false);
  assert.equal(source.includes('sendBeacon'), false);
});
