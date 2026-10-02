import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Remove background colors from the login screens so body::before grid shows through
    text = re.sub(r'#loginScreen\s*\{[^}]*background:[^;]+;', lambda m: m.group(0).replace(m.group(0).split('background:')[-1], ' transparent;'), text)
    text = re.sub(r'#schoolLoginScreen\s*\{[^}]*background:[^;]+;', lambda m: m.group(0).replace(m.group(0).split('background:')[-1], ' transparent;'), text)
    
    # 2. Aggressively rewrite ALL .pin-input CSS in the document
    old_pin_css = re.search(r'\.pin-input\s*\{.*?\.pin-input:focus\s*\{.*?\}', text, flags=re.DOTALL)
    if old_pin_css:
        new_pin_css = '''
    .pin-input {
      width: 100%; padding: 14px 16px; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
      font-size: 16px; font-weight: 800; text-align: center; outline: none; color: #fff;
      background: rgba(255,255,255,0.05); transition: border-color .3s, background .3s;
    }
    .pin-input::placeholder { color: rgba(255,255,255,0.3); font-weight: 600; font-size: 13px; letter-spacing: 0px; }
    .pin-input:focus { border-color: rgba(241, 196, 15, 0.5); background: rgba(255,255,255,0.1); box-shadow: 0 0 10px rgba(241, 196, 15, 0.2); }
'''
        text = text.replace(old_pin_css.group(0), new_pin_css)
    else:
        # manual fallback if regex fails
        text = re.sub(r'\.pin-input\s*\{[^}]*\}', '.pin-input { width: 100%; padding: 14px 16px; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; font-size: 16px; font-weight: 800; text-align: center; outline: none; color: #fff; background: rgba(255,255,255,0.05); transition: border-color .3s, background .3s; }', text)
        text = re.sub(r'\.pin-input:focus\s*\{[^}]*\}', '.pin-input:focus { border-color: rgba(241, 196, 15, 0.5); background: rgba(255,255,255,0.1); box-shadow: 0 0 10px rgba(241, 196, 15, 0.2); }', text)
        text = re.sub(r'\.pin-input::placeholder\s*\{[^}]*\}', '.pin-input::placeholder { color: rgba(255,255,255,0.3); font-weight: 600; font-size: 13px; letter-spacing: 0px; }', text)
        text = re.sub(r'background:\s*#F9FBFC;', 'background: rgba(255,255,255,0.05);', text)
        text = re.sub(r'background:\s*#FFF;', 'background: rgba(255,255,255,0.1);', text)

    # 3. Upgrade the Return link to look like a premium button or nicely styled text
    text = re.sub(r'<a href="index\.html"[^>]*>([^<]+)</a>', r'<a href="index.html" class="return-link" style="display:inline-block; margin-top:20px; font-size:13px; font-weight:700; color:rgba(255,255,255,0.5); text-decoration:none; padding:8px 16px; border-radius:20px; background:rgba(255,255,255,0.05); transition:all 0.3s;" onmouseover="this.style.background=\'rgba(255,255,255,0.1)\'; this.style.color=\'#fff\';" onmouseout="this.style.background=\'rgba(255,255,255,0.05)\'; this.style.color=\'rgba(255,255,255,0.5)\';">\1</a>', text)
    # Ensure IDs are preserved if they were there (aReturn, sReturn)
    if 'id="aReturn"' not in text and '教练' in text:
        text = text.replace('class="return-link"', 'class="return-link" id="aReturn"')
    if 'id="sReturn"' not in text and '校际赛' in text:
        text = text.replace('class="return-link"', 'class="return-link" id="sReturn"')
        
    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(text)

print("Inputs, backgrounds, and return links fixed.")
