import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'\.l-card\s*\{[^}]*\}', text):
    print(m.group(0))

for m in re.finditer(r'\.podium-card\s*\{[^}]*\}', text):
    print(m.group(0))
