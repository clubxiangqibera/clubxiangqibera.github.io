import io, sys
sys.stdout.reconfigure(encoding='utf-8')

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="appleMegaMenu"')
idx2 = text.find('<!-- END APPLE MEGA MENU -->', idx1)
if idx2 == -1:
    idx2 = text.find('</div>\n</div>', idx1) + 14
print(text[idx1:idx1+1500])
