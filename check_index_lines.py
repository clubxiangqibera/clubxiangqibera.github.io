import io, sys
sys.stdout.reconfigure(encoding='utf-8')

with io.open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
idx = c.find('id="appleMegaMenu"')
block = c[idx:idx+900]
for line in block.split('\n'):
    if '<a ' in line or '<h4' in line:
        print('  ', line.strip())
