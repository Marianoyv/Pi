"""Fail the local release if its analytics runtime or static dependencies are missing."""
from pathlib import Path
from html.parser import HTMLParser
import json,re

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
errors=[]
class Assets(HTMLParser):
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        for key in ('src','href'):
            value=values.get(key,'').split('?',1)[0]
            if value.startswith('/static/') and not (DIST/value.lstrip('/')).is_file():
                errors.append('Missing asset: '+value)

pages=list(DIST.rglob('*.html'))
if not pages: errors.append('No exported HTML pages found.')
for page in pages:
    html=page.read_text(encoding='utf-8')
    Assets().feed(html)
    if 'data-analytics-banner' in html:errors.append('Legacy analytics banner must not be exported: '+str(page.relative_to(DIST)))
    if 'data-analytics-preferences' in html:
        if html.count('web/js/analytics.js')!=1:errors.append('Analytics must have exactly one runtime: '+str(page.relative_to(DIST)))
        if not re.search(r'data-measurement-id="G-[A-Z0-9]+"',html):errors.append('Missing GA4 measurement ID.')
        if 'googletagmanager.com/gtag/js' in html:errors.append('Google tag must be loaded by the consent-mode runtime: '+str(page.relative_to(DIST)))
        for choice in ('granted','denied','disabled'):
            if 'data-analytics-consent="'+choice+'"' not in html:errors.append('Missing consent choice: '+choice)
finance_root=DIST/'finance'
finance_pages=list(finance_root.rglob('*.html')) if finance_root.is_dir() else []
if len(finance_pages)<22:errors.append('Pi Finance export is incomplete.')
for page in finance_pages:
    html=page.read_text(encoding='utf-8')
    if 'indices-argentinos.web.app' in html or 'Índices Argentinos' in html:
        errors.append('Legacy finance brand or domain remains: '+str(page.relative_to(DIST)))
    for match in re.findall(r'(?:href|src)="(/finance/[^"?#]*)',html):
        target=DIST/match.lstrip('/')
        if match.endswith('/'):
            target=target/'index.html'
        if not target.is_file():errors.append('Missing Pi Finance dependency: '+match)
if not (DIST/'index.html').is_file() or 'data-analytics-preferences' not in (DIST/'index.html').read_text(encoding='utf-8'):
    errors.append('Homepage analytics integration is missing.')
for required in ('analytics.js','vendor/web-vitals.js','vendor/web-vitals-LICENSE.txt','vendor/web-vitals-NOTICE.txt'):
    if not (DIST/'static/web/js'/required).is_file():errors.append('Missing analytics dependency: '+required)
analytics_runtime=(DIST/'static/web/js/analytics.js')
if analytics_runtime.is_file():
    analytics_source=analytics_runtime.read_text(encoding='utf-8')
    if "const analyticsGranted = { ...denied, analytics_storage: 'granted' };" not in analytics_source:
        errors.append('Analytics storage must be enabled by default.')
    if "window.gtag('consent', 'default', analyticsGranted);" not in analytics_source:
        errors.append('Analytics default must be applied before configuration.')
for file in DIST.rglob('*'):
    if file.is_file() and (file.name.startswith('.env') or file.name=='analytics-reader.json' or 'credentials' in file.relative_to(DIST).parts):errors.append('Private file in static output: '+str(file.relative_to(DIST)))
hosting=json.loads((ROOT/'firebase.json').read_text(encoding='utf-8'))['hosting']
if hosting.get('public')!='dist':errors.append('Firebase Hosting must publish dist.')
if hosting.get('rewrites'):errors.append('Unexpected backend rewrite in static Hosting configuration.')
if errors:
    raise SystemExit('\n'.join(sorted(set(errors))))
print(f'Release check passed: {len(pages)} HTML files, full analytics enabled by default, complete performance assets, no private build inputs.')
