#!/usr/bin/env python3
"""Inject common nav + footer into all HTML pages without modifying content."""

import re, os

REPO = "/home/workspace/Projects/cbse-osm-osint"
PAGES = [f for f in os.listdir(REPO) if f.endswith(".html")]

NAV_HTML = '''
<div class="site-nav">
  <div class="site-nav-inner">
    <a href="index.html" class="site-nav-brand">CBSE OSM<span class="site-nav-sep">/</span>OSINT</a>
    <nav>
      <a href="index.html">Home</a>
      <a href="know-your-coempt.html">Coempt</a>
      <a href="know-your-examtech.html">ExamTech</a>
      <a href="impacted-entities.html">Entities</a>
      <a href="annexure.html">Annexure</a>
      <a href="api-surface.html">API</a>
      <a href="terms-of-reference.html">TOR</a>
    </nav>
  </div>
</div>
'''

FOOTER_HTML = '''
<footer class="site-footer">
  <div class="site-footer-inner">
    <p>CBSE OSM OSINT Investigation &middot; Published May&ndash;Jun 2026 &middot; <a href="https://github.com/CCAgentOrg/cbse-osm-osint">Source</a> &middot; <a href="https://zo.pub/cashlessconsumer/cbse-osm-onmarks-osint">Evidence Archive</a></p>
  </div>
</footer>
'''

# Cloudflare Web Analytics beacon (replace PLACEHOLDER_TOKEN with your site token)
# Get a token at: https://dash.cloudflare.com → Web Analytics → Add Site
CF_ANALYTICS_SCRIPT = '''
<!-- Cloudflare Web Analytics -->
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "PLACEHOLDER_TOKEN", "spa": true}'></script>
<script>
window.addEventListener('load', function() {
  function trackEvent(name, data) {
    if (window.cloudflare && window.cloudflare.insights) {
      window.cloudflare.insights.trackEvent({ name: name, data: data || {} });
    }
  }
  document.querySelectorAll('.site-nav nav a').forEach(function(a) {
    a.addEventListener('click', function() {
      trackEvent('nav_click', { page: a.textContent.trim(), href: a.href });
    });
  });
  document.querySelectorAll('.path-step a').forEach(function(a) {
    a.addEventListener('click', function() {
      trackEvent('reading_path_click', { title: a.textContent.trim(), href: a.href });
    });
  });
  document.querySelectorAll('.card-link').forEach(function(a) {
    a.addEventListener('click', function() {
      trackEvent('card_click', { label: a.textContent.trim(), href: a.href });
    });
  });
  document.querySelectorAll('.featured a[href^="http"]').forEach(function(a) {
    a.addEventListener('click', function() {
      trackEvent('source_link_click', { href: a.href, text: a.textContent.trim().substring(0, 60) });
    });
  });
});
</script>
'''

NAV_CSS = '''
/* === COMMON SITE NAV & FOOTER === */
.site-nav{background:#fff;border-bottom:1px solid #e0dcd4;position:sticky;top:0;z-index:100;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.site-nav-inner{max-width:960px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:48px;gap:12px;flex-wrap:wrap}
.site-nav-brand{font-weight:700;font-size:.9em;color:#1a1a1a;text-decoration:none;letter-spacing:-.01em;white-space:nowrap}
.site-nav-sep{color:#c4a0a0;margin:0 2px}
.site-nav nav{display:flex;gap:4px;flex-wrap:wrap}
.site-nav nav a{font-size:.78em;padding:6px 10px;color:#666;text-decoration:none;border-radius:4px;white-space:nowrap;transition:background .15s,color .15s}
.site-nav nav a:hover{background:#f5f2eb;color:#8b1a1a}
.site-nav nav a.active{background:#8b1a1a;color:#fff}
.site-footer{border-top:1px solid #e0dcd4;padding:24px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin-top:60px}
.site-footer-inner{max-width:960px;margin:0 auto;padding:0 24px;text-align:center}
.site-footer p{font-size:.82em;color:#888;line-height:1.6}
.site-footer a{color:#8b1a1a;text-decoration:none;border-bottom:1px solid #c4a0a0}
.site-footer a:hover{color:#5a0f0f}
@media(max-width:600px){
  .site-nav-inner{flex-direction:column;height:auto;padding:10px 16px;gap:8px}
  .site-nav nav{gap:2px;justify-content:center}
  .site-nav nav a{padding:4px 8px;font-size:.75em}
  .site-footer{padding:16px}
  .site-footer-inner{padding:0 16px}
}
@media(prefers-color-scheme:dark){
  .site-nav{background:#161b22;border-bottom-color:#30363d}
  .site-nav-brand{color:#f0f6fc}
  .site-nav nav a{color:#8b949e}
  .site-nav nav a:hover{background:#21262d;color:#58a6ff}
  .site-nav nav a.active{background:#238636;color:#fff}
  .site-footer{border-top-color:#30363d}
  .site-footer p{color:#484f58}
  .site-footer a{color:#58a6ff;border-bottom-color:#1f3a5f}
  .site-footer a:hover{color:#79c0ff}
}
'''

def inject_page(filepath, nav_html, footer_html, nav_css, analytics_script=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already injected
    if 'class="site-nav"' in html:
        print(f"  SKIP {filepath} (already has site-nav)")
        return

    # Inject nav right after <body> (handle <body> with or without attributes)
    html = re.sub(
        r'(<body[^>]*>)',
        r'\1' + nav_html,
        html,
        count=1
    )

    # Inject footer + analytics before </body>
    before_body_close = footer_html
    if analytics_script and 'cloudflareinsights' not in html:
        before_body_close += analytics_script
    html = html.replace('</body>', before_body_close + '\n</body>', 1)

    # Inject nav CSS into <style> block (append to first <style>)
    if '<style>' in html:
        html = html.replace('<style>', '<style>\n' + nav_css, 1)
    else:
        # Create a style block in head
        html = html.replace('</head>', '<style>\n' + nav_css + '\n</style>\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  OK   {filepath}")

for page in sorted(PAGES):
    path = os.path.join(REPO, page)
    inject_page(path, NAV_HTML, FOOTER_HTML, NAV_CSS, CF_ANALYTICS_SCRIPT)

print(f"\nDone: {len(PAGES)} pages processed")
