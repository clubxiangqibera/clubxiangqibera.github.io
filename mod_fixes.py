import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Partner Logos
html = re.sub(
    r'<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:32px; margin-top:20px; opacity:0\.8;">.*?</div>',
    '<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:32px; margin-top:20px; opacity:0.8;">\n        <span style="font-family: var(--font-serif); font-size:1.15rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:0.05em;">Persatuan Catur Cina Daerah Bera</span>\n      </div>',
    html, flags=re.DOTALL
)

# 2. Fix the Hero Panel Color in the injected CSS
# I previously injected cxb-theme.css into index.html's <style> block.
# I need to find the .hero class in index.html's <style> and replace its background.
# The user wants the rich blue color for the panel instead of the dull gray-navy.
html = html.replace(
    'background: linear-gradient(180deg, var(--navy-800), var(--navy-900));',
    'background: linear-gradient(145deg, #061724 0%, #0E2F44 55%, #1A5276 100%);'
)

# 3. Make the background color richer (less "gray")
html = html.replace('--navy-950: #07101e;', '--navy-950: #040c17;')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed partners and restored rich blue hero gradient!')
