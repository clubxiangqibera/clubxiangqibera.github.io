import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('loginScreen', idx)
    if idx == -1: break
    print('Found at', idx, ':', text[max(0, idx-30):idx+80])
    idx += 11
