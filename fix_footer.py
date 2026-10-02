import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Logo
text = text.replace('src="cxb_round_emblem.png" alt="Persatuan Logo"', 'src="persatuan_emblem.png" alt="Persatuan Logo"')

# 2. Fix footer width by appending to the CSS
css_fix = '''
/* Fix footer width */
.footer { width: 100%; margin-top: auto; }
'''
text = text.replace('</style>', css_fix + '</style>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with io.open('cxb-theme.css', 'r', encoding='utf-8') as f:
    css = f.read()
css += css_fix
with io.open('cxb-theme.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated logo and fixed footer width!')
