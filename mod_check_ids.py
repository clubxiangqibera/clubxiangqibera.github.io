import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<div id="[^"]+"', text):
    print(m.group(0))
