import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function toggleMainNav')
print(text[idx:idx+700])
