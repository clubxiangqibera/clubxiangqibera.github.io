import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# --- INDEX.HTML FIXES ---
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove emojis and convert Language vertical links to Apple Segmented Control
old_lang_col = r'''<div class="apple-mega-col">
      <h4 data-i18n="nav.language">系统语言 \(Language\)</h4>
      <a onclick="setLang\('cn'\); closeMainNav\(\)">🇨🇳 中文 \(Chinese\)</a>
      <a onclick="setLang\('bm'\); closeMainNav\(\)">🇲🇾 Bahasa Melayu</a>
      <a onclick="setLang\('en'\); closeMainNav\(\)">🇬🇧 English</a>
    </div>'''

new_lang_col = '''<div class="apple-mega-col">
      <h4 data-i18n="nav.language">系统语言 (Language)</h4>
      <div class="apple-segment">
        <button id="seg_cn" class="seg-btn active" onclick="setLang('cn'); updateSeg('cn'); closeMainNav()">中文</button>
        <button id="seg_bm" class="seg-btn" onclick="setLang('bm'); updateSeg('bm'); closeMainNav()">Melayu</button>
        <button id="seg_en" class="seg-btn" onclick="setLang('en'); updateSeg('en'); closeMainNav()">English</button>
      </div>
    </div>'''

text = re.sub(old_lang_col, new_lang_col, text)

# Inject Apple Segment CSS and JS logic for index.html
apple_seg_css = '''
/* Apple Style Segmented Control */
.apple-segment {
  display: flex;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 4px;
  width: 100%;
  max-width: 300px;
}
.apple-segment .seg-btn {
  flex: 1;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  padding: 10px 0;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.apple-segment .seg-btn.active {
  background: rgba(255, 255, 255, 0.95);
  color: #111;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
'''
text = text.replace('</style>', apple_seg_css + '\n</style>')

seg_js = '''
function updateSeg(lang) {
  document.querySelectorAll('.apple-segment .seg-btn').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById('seg_' + lang);
  if(activeBtn) activeBtn.classList.add('active');
}
'''
text = text.replace('// --- END MAIN NAV SYSTEM ---', '// --- END MAIN NAV SYSTEM ---\n' + seg_js)


# 2. Fix Missing Translations in index.html (events.title missing in BM and EN)
# Search for BM block
bm_inject = '''    "gallery.empty": "Tiada album awam setakat ini.",
    "events.title": "Pusat Acara & Aktiviti",
    "events.sub": "Sumber dan Rekod Acara CXQB",'''
text = text.replace('"gallery.empty": "Tiada album awam setakat ini.",', bm_inject)

# Search for EN block
en_inject = '''    "gallery.empty": "No public albums available.",
    "events.title": "Events & Activities Center",
    "events.sub": "CXQB Event Resources and Records",'''
text = text.replace('"gallery.empty": "No public albums available.",', en_inject)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# --- ADMIN.HTML & SCHOOL.HTML FIXES ---
admin_css = '''
/* Apple Style Segmented Control */
.lang-switcher {
  display: flex;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  padding: 4px;
  margin: 0 auto 24px auto;
  width: 200px;
}
.lang-switcher span {
  flex: 1;
  background: transparent;
  color: #64748B;
  padding: 8px 0;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
  display: flex; justify-content: center; align-items: center;
}
.lang-switcher span.active {
  background: #FFF;
  color: #0F172A;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
'''

for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject CSS
    content = content.replace('</style>', admin_css + '\n</style>')
    
    # Replace old lang switcher HTML
    old_admin_lang = re.search(r'<div class="lang-switcher">.*?</div>', content, flags=re.DOTALL)
    if old_admin_lang:
        new_admin_lang = '''<div class="lang-switcher">
      <span id="langCn" class="active" onclick="setLang('cn')">中文</span>
      <span id="langEn" onclick="setLang('en')">English</span>
    </div>'''
        content = content.replace(old_admin_lang.group(0), new_admin_lang)
    
    # Remove the `|` inline styles just in case it wasn't matched fully
    
    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Apple Segmented Controls and Translations Applied!")
