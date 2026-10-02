import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<div class="ph-header">')
e = text.find('<!-- 2. CAMP PROMO BANNER -->')
print(text[s:e])
