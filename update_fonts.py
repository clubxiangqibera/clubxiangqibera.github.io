import re

for file in ['index.html', 'admin.html', 'school.html']:
    html = open(file, encoding='utf-8').read()
    
    # 1. Add Noto Serif SC to Google Fonts link
    html = re.sub(
        r'(family=Noto\+Sans\+SC:wght@[^&]+)',
        r'\1&family=Noto+Serif+SC:wght@400;500;600;700;900',
        html
    )
    
    # 2. Update .apple-mega-col h4 CSS
    html = re.sub(
        r'(\.apple-mega-col h4 \{.*?)(font-weight: 800;)',
        r"\1font-family: 'Noto Serif SC', var(--font-serif); font-weight: 600;",
        html,
        flags=re.DOTALL
    )
    
    # 3. Update .apple-mega-col a CSS
    html = re.sub(
        r'(\.apple-mega-col a \{.*?)(font-weight: 700;)(.*?font-family: var\(--font-serif\);)',
        r"\1font-weight: 500;\3",
        html,
        flags=re.DOTALL
    )
    # Remove the old font-family: var(--font-serif) from  tags
    html = re.sub(
        r'(\.apple-mega-col a \{.*?)(font-family: var\(--font-serif\);)',
        r"\1font-family: var(--font-sans);",
        html,
        flags=re.DOTALL
    )
    
    open(file, 'w', encoding='utf-8').write(html)
    print(f'Updated fonts in {file}')
