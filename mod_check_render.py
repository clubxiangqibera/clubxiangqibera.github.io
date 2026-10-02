import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function renderPublicLadder[\s\S]*?\}', text)
if m: print(m.group(0))
