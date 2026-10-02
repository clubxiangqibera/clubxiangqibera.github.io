import io, re
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<div class="lang-switcher">.*?</div>', text, flags=re.DOTALL)
if match: print(match.group(0))
