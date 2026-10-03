import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('public-nav-bar')
print('=== CONTEXT BEFORE public-nav-bar ===')
print(text[max(0, idx-400):idx+300])
