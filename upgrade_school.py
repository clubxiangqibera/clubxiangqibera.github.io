import io, re
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update .school-login-card CSS to match the deep navy translucent style
old_school_card = r'\.school-login-card\s*\{[^\}]*\}'
new_school_card = '.school-login-card { background: rgba(6,23,36,0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 28px; padding: 36px 40px 36px; width: 100%; max-width: 530px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); text-align: center; position: relative; backdrop-filter: blur(20px); }'
text = re.sub(old_school_card, new_school_card, text)

# 2. Update .lang-switch and .lang-btn for Apple-style Segmented Control in school.html
old_lang_switch = r'\.lang-switch\s*\{[^\}]*\}'
new_lang_switch = '.lang-switch { display: inline-flex; background: rgba(255,255,255,0.08); border-radius: 10px; padding: 4px; border: none; width: 200px; justify-content: center; }'
text = re.sub(old_lang_switch, new_lang_switch, text)

old_lang_btn = r'\.lang-btn\s*\{[^\}]*\}'
new_lang_btn = '.lang-btn { flex: 1; padding: 8px 0; border-radius: 8px; font-size: 13px; font-weight: 700; border: none; cursor: pointer; background: transparent; color: rgba(255,255,255,0.5); transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); display: flex; justify-content: center; align-items: center; }'
text = re.sub(old_lang_btn, new_lang_btn, text)

old_lang_btn_active = r'\.lang-btn\.active\s*\{[^\}]*\}'
new_lang_btn_active = '.lang-btn.active { background: rgba(255,255,255,0.9); color: #000; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }'
text = re.sub(old_lang_btn_active, new_lang_btn_active, text)

# 3. Text colors in school-login-card (H1, p, return links)
text = re.sub(r'color:\s*var\(--pri\)', 'color: #fff', text)
text = re.sub(r'color:\s*var\(--text2\)', 'color: rgba(255,255,255,0.6)', text)
text = re.sub(r'color:\s*var\(--text3\)', 'color: rgba(255,255,255,0.5)', text)
text = re.sub(r'color:\s*#334155', 'color: rgba(255,255,255,0.6)', text)
text = re.sub(r'color:\s*#1A5276', 'color: rgba(255,255,255,0.8)', text)

# 4. Make the input pin-input match
text = re.sub(r'background:\s*#FAFBFD', 'background: rgba(255,255,255,0.05)', text)
text = re.sub(r'border:\s*2px solid var\(--border\)', 'border: 1px solid rgba(255,255,255,0.1)', text)
text = text.replace('color: var(--pri);', 'color: #fff;')

# 5. Fix the submit button in school.html which uses inline styles
# It uses background:linear-gradient(135deg, #0E2F44 0%, #1A5276 100%) or similar
text = re.sub(r'background:linear-gradient\(.*?1A5276.*?\)', 'background:#040C17; border: 1px solid rgba(255,255,255,0.1)', text)
text = text.replace('border-radius:12px;', 'border-radius:12px; font-weight:800; color:#fff;')

# Apply animation class to the login card just in case it wasn't there
text = text.replace('class="school-login-card"', 'class="school-login-card animate-zoom"')
if 'animate-zoom' not in text:
    pass # we added it in the previous script

with io.open('school.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("School HTML explicitly upgraded!")
