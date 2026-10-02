import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('gallery')
while idx != -1:
    print(text[max(0, idx-30):min(len(text), idx+100)])
    idx = text.find('gallery', idx+1)
