import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'\.podium-box\s*\{[^}]*\}', text):
    print(m.group(0))

for m in re.finditer(r'\.rank-item\s*\{[^}]*\}', text):
    print(m.group(0))
    
for m in re.finditer(r'\.gate-card\s*\{[^}]*\}', text):
    print(m.group(0))
