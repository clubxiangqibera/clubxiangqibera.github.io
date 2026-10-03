import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('toggleMainNav', idx)
    if idx == -1: break
    print('Found at', idx, ':', text[max(0, idx-20):idx+300])
    idx += 13
