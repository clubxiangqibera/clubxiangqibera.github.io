import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('public-nav-bar', idx)
    if idx == -1: break
    print('Found at', idx)
    print(text[max(0, idx-50):idx+300])
    idx += 14
