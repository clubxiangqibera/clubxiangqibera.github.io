import io, re
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<div class="school-login-card.*?</div>\s*</div>', text, flags=re.DOTALL)
if match:
    print(match.group(0)[:800])
