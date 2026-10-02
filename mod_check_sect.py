import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\.section-title\s*\{[^}]*\}', text)
if m: print(m.group(0))

m = re.search(r'\.section-sub\s*\{[^}]*\}', text)
if m: print(m.group(0))
