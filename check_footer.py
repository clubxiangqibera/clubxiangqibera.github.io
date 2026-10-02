import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('<footer class="footer">')
print(text[idx-500:idx+50])
