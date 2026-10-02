import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('ladder')
print('Ladder index:', idx)
print(text[max(0, idx-100):min(len(text), idx+300)])

idx = text.find('publicPodiumArea')
print('publicPodiumArea index:', idx)
if idx != -1:
    print(text[max(0, idx-100):min(len(text), idx+300)])
