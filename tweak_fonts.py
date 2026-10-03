import re

for file in ['index.html', 'admin.html', 'school.html']:
    html = open(file, encoding='utf-8').read()
    
    html = re.sub(
        r'(\.apple-mega-col a \{.*?)(font-weight: 500;)',
        r"\1font-weight: 400;",
        html,
        flags=re.DOTALL
    )
    
    open(file, 'w', encoding='utf-8').write(html)
    print(f'Tweaked font-weight in {file}')
