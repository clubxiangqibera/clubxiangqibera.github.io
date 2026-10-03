import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<header class="public-nav-bar"')
print(text[max(0, idx-200):idx+300])
