import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'#securityGate\s*\{[^}]*\}', text)
if m: print(m.group(0))

m = re.search(r'\.public-hero\s*\{[^}]*\}', text)
if m: print(m.group(0))

m = re.search(r'\.public-content-wrap\s*\{[^}]*\}', text)
if m: print(m.group(0))
