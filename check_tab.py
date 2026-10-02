import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function togglePublicTab')
print(text[idx:idx+800])
