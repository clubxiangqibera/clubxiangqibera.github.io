import io, re
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find the security gate or login section in admin
match = re.search(r'<div[^>]*id="securityGate"[^>]*>.*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if match:
    print(match.group(0)[:800])
else:
    match2 = re.search(r'<div[^>]*login[^>]*>.*?</div>', text, flags=re.IGNORECASE)
    if match2:
        print(match2.group(0)[:800])
