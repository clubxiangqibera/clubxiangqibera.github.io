import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Prevent sidebar from closing when language is switched
# Find the language buttons in the nav sidebar and remove closeMainNav()
old_cn = r'''<button onclick="setLang\('cn', this\); closeMainNav\(\)" class="lang-btn"'''
new_cn = r'''<button onclick="setLang('cn', this)" class="lang-btn"'''
text = re.sub(old_cn, new_cn, text)

old_bm = r'''<button onclick="setLang\('bm', this\); closeMainNav\(\)" class="lang-btn"'''
new_bm = r'''<button onclick="setLang('bm', this)" class="lang-btn"'''
text = re.sub(old_bm, new_bm, text)

old_en = r'''<button onclick="setLang\('en', this\); closeMainNav\(\)" class="lang-btn"'''
new_en = r'''<button onclick="setLang('en', this)" class="lang-btn"'''
text = re.sub(old_en, new_en, text)

# 2. Add "Auto Zoom" (pop-in) animation to the login card
css_animation = '''
@keyframes popZoom {
  0% { opacity: 0; transform: scale(0.9) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-zoom {
  animation: popZoom 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
'''
text = text.replace('</style>', css_animation + '\n</style>')

# Apply animation class to gate-card
old_gate = r'<div class="gate-card" style="margin:20px auto; width: 100%; max-width: 440px;'
new_gate = r'<div class="gate-card animate-zoom" style="margin:20px auto; width: 100%; max-width: 440px;'
text = text.replace(old_gate, new_gate)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Zoom animation added and sidebar lang issue fixed.")
