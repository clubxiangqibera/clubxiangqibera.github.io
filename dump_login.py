import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('publicLoginSection')
if idx != -1:
    print(text[max(0, idx-100):idx+2500])
