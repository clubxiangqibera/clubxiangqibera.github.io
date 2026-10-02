import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
old_archive_css = r'''\.archive-view \{
  position: fixed; inset: 0; z-index: 8000;
  background: var\(--navy-950\);
  overflow-y: auto; display: none;
\}'''
new_archive_css = '''.archive-view {
  position: fixed; top: 0; right: -100%; width: 100%; max-width: 480px; height: 100vh;
  z-index: 8000; background: var(--navy-950);
  border-left: 1px solid var(--line);
  box-shadow: -10px 0 40px rgba(0,0,0,0.6);
  overflow-y: auto; transition: right 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.archive-view.open { right: 0; }
.archive-backdrop {
  position: fixed; inset: 0; background: rgba(7, 16, 30, 0.8);
  z-index: 7999; backdrop-filter: blur(4px);
  opacity: 0; pointer-events: none; transition: opacity 0.3s;
}
.archive-backdrop.open { opacity: 1; pointer-events: auto; }
.archive-view__body .events-grid { grid-template-columns: 1fr; gap: 20px; }
'''
text = re.sub(old_archive_css, new_archive_css, text)

# 2. Update HTML (Inject backdrop before eventsArchiveView)
old_html = r'<div id="eventsArchiveView" class="archive-view">'
new_html = '''<div id="eventsArchiveBackdrop" class="archive-backdrop" onclick="closeArchiveView()"></div>
<div id="eventsArchiveView" class="archive-view">'''
text = text.replace(old_html, new_html)

# Also update the close button text from "⬅ 返回首页 (Back)" to "➡ 收起 (Close)"
text = text.replace('⬅ 返回首页 (Back)', '➡ 收起 (Close)')

# 3. Update JS
old_js_open = "document.getElementById('eventsArchiveView').style.display = 'block';"
new_js_open = "document.getElementById('eventsArchiveView').classList.add('open'); document.getElementById('eventsArchiveBackdrop').classList.add('open');"
text = text.replace(old_js_open, new_js_open)

old_js_close = "document.getElementById('eventsArchiveView').style.display = 'none';"
new_js_close = "document.getElementById('eventsArchiveView').classList.remove('open'); document.getElementById('eventsArchiveBackdrop').classList.remove('open');"
text = text.replace(old_js_close, new_js_close)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Sidebar applied!")
