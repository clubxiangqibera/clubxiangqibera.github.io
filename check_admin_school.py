import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<div[^>]*id="securityGate"[^>]*>.*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if match:
    print("MATCH 1:\n", match.group(0)[:800])
else:
    match2 = re.search(r'<div[^>]*id="securityGate"[^>]*>.*?(?=<div id="app")' , text, flags=re.DOTALL|re.IGNORECASE)
    if match2:
        print("MATCH 2:\n", match2.group(0)[:1200])

with io.open('school.html', 'r', encoding='utf-8') as f:
    text2 = f.read()
match_s = re.search(r'<div[^>]*id="securityGate"[^>]*>.*?(?=<div id="app")' , text2, flags=re.DOTALL|re.IGNORECASE)
if match_s:
    print("SCHOOL MATCH:\n", match_s.group(0)[:1200])
