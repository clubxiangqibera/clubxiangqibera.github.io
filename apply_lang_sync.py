import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# ================= INDEX.HTML =================
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add localStorage to index.html's setLang
old_setLang = r'function setLang\(lang, btnContext\) \{'
new_setLang = '''function setLang(lang, btnContext) {
    let prefLang = lang === 'cn' ? 'zh' : lang;
    localStorage.setItem('cxb_lang_pref', prefLang);'''
text = re.sub(old_setLang, new_setLang, text)

# 2. Add onload loader for index.html
loader_js = '''
document.addEventListener('DOMContentLoaded', () => {
  let saved = localStorage.getItem('cxb_lang_pref');
  if(saved) {
    let internalLang = saved === 'zh' ? 'cn' : saved;
    setLang(internalLang);
    if(typeof updateSeg === 'function') updateSeg(internalLang);
  }
});
'''
text = text.replace('// --- END MAIN NAV SYSTEM ---', '// --- END MAIN NAV SYSTEM ---\n' + loader_js)
with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# ================= ADMIN.HTML =================
with io.open('admin.html', 'r', encoding='utf-8') as f:
    admin_text = f.read()

# Update CSS for admin.html lang-switch
old_admin_switch = r'\.lang-switch\s*\{[^\}]*\}'
new_admin_switch = '.lang-switch { display: inline-flex; background: rgba(255,255,255,0.08); border-radius: 10px; padding: 4px; border: none; width: 260px; justify-content: center; margin: 0 auto; }'
if re.search(old_admin_switch, admin_text):
    admin_text = re.sub(old_admin_switch, new_admin_switch, admin_text)
else:
    admin_text = admin_text.replace('</style>', new_admin_switch + '\n</style>')

old_admin_btn = r'\.lang-btn\s*\{[^\}]*\}'
new_admin_btn = '.lang-btn { flex: 1; padding: 8px 0; border-radius: 8px; font-size: 13px; font-weight: 700; border: none; cursor: pointer; background: transparent; color: rgba(255,255,255,0.5); transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); display: flex; justify-content: center; align-items: center; }'
if re.search(old_admin_btn, admin_text):
    admin_text = re.sub(old_admin_btn, new_admin_btn, admin_text)
else:
    admin_text = admin_text.replace('</style>', new_admin_btn + '\n</style>')

old_admin_active = r'\.lang-btn\.active\s*\{[^\}]*\}'
new_admin_active = '.lang-btn.active { background: rgba(255,255,255,0.9); color: #000; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }'
if re.search(old_admin_active, admin_text):
    admin_text = re.sub(old_admin_active, new_admin_active, admin_text)
else:
    admin_text = admin_text.replace('</style>', new_admin_active + '\n</style>')

# Replace admin lang HTML
old_admin_html = r'<div class="lang-switch">.*?</div>'
new_admin_html = '''<div class="lang-switch">
        <button type="button" class="lang-btn active" id="aLangZh" onclick="setAdminLang('zh')">中文</button>
        <button type="button" class="lang-btn" id="aLangBm" onclick="setAdminLang('bm')">Melayu</button>
        <button type="button" class="lang-btn" id="aLangEn" onclick="setAdminLang('en')">English</button>
      </div>'''
admin_text = re.sub(old_admin_html, new_admin_html, admin_text, flags=re.DOTALL)

# Update setAdminLang in admin.html
admin_setlang = r'function setAdminLang\(lang\) \{'
admin_setlang_new = '''function setAdminLang(lang) {
      localStorage.setItem('cxb_lang_pref', lang);
      document.querySelectorAll('.lang-switch .lang-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('aLang' + lang.charAt(0).toUpperCase() + lang.slice(1));
      if(activeBtn) activeBtn.classList.add('active');
'''
admin_text = re.sub(admin_setlang, admin_setlang_new, admin_text)

# Ensure BM is handled in admin.html translation logic
if 'if(lang === \'zh\')' in admin_text:
    bm_logic = '''
      if(lang === 'bm') {
        document.getElementById('adminPinInput').placeholder = 'Masukkan Kata Laluan';
        document.getElementById('aBtn').textContent = '🔐 Log Masuk Admin';
        document.getElementById('loginError').textContent = '❌ Kata Laluan Tidak Sah';
        document.getElementById('aReturn').textContent = '← Kembali ke Utama (Return)';
      }
'''
    admin_text = admin_text.replace("if(lang === 'zh') {", bm_logic + "      if(lang === 'zh') {")

admin_loader = '''
window.addEventListener('DOMContentLoaded', () => {
  let saved = localStorage.getItem('cxb_lang_pref');
  if(saved) setAdminLang(saved);
});
'''
admin_text = admin_text.replace('</script>\n</body>', admin_loader + '\n</script>\n</body>')
with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_text)

# ================= SCHOOL.HTML =================
with io.open('school.html', 'r', encoding='utf-8') as f:
    school_text = f.read()

# Update CSS for school.html lang-switch
# We already did some of this, but let's make it 3-button width
school_text = re.sub(r'width:\s*200px;', 'width: 260px;', school_text)

# Replace school lang HTML
old_school_html = r'<div class="lang-switch">.*?</div>'
new_school_html = '''<div class="lang-switch">
        <button type="button" class="lang-btn active" id="btnLangZh" onclick="setLoginLang('zh')">中文</button>
        <button type="button" class="lang-btn" id="btnLangBm" onclick="setLoginLang('bm')">Melayu</button>
        <button type="button" class="lang-btn" id="btnLangEn" onclick="setLoginLang('en')">English</button>
      </div>'''
school_text = re.sub(old_school_html, new_school_html, school_text, count=1, flags=re.DOTALL) # only the gate one first

# Update setLoginLang in school.html
school_setlang = r'function setLoginLang\(lang\) \{'
school_setlang_new = '''function setLoginLang(lang) {
      localStorage.setItem('cxb_lang_pref', lang);
      document.querySelectorAll('.lang-switch .lang-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('btnLang' + lang.charAt(0).toUpperCase() + lang.slice(1));
      if(activeBtn) activeBtn.classList.add('active');
'''
school_text = re.sub(school_setlang, school_setlang_new, school_text)

if 'if(lang === \'zh\')' in school_text:
    bm_logic_school = '''
      if(lang === 'bm') {
        document.getElementById('schoolPinInput').placeholder = 'Kod Kebenaran (cth: CXQB-8888)';
        document.getElementById('sBtn').textContent = '🛡️ Sahkan & Masuk (Verify)';
        document.getElementById('sError').textContent = '❌ Kod Tidak Sah';
        document.getElementById('sReturn').textContent = '← Kembali ke Utama (Return)';
      }
'''
    school_text = school_text.replace("if(lang === 'zh') {", bm_logic_school + "      if(lang === 'zh') {")

school_loader = '''
window.addEventListener('DOMContentLoaded', () => {
  let saved = localStorage.getItem('cxb_lang_pref');
  if(saved) setLoginLang(saved);
});
'''
school_text = school_text.replace('</script>\n</body>', school_loader + '\n</script>\n</body>')
with io.open('school.html', 'w', encoding='utf-8') as f:
    f.write(school_text)

print("Language memory and unified Apple segmented switcher added to all apps!")
