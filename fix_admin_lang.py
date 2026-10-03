import re

html = open('admin.html', encoding='utf-8').read()

# Fix the aLangZh missing element crash
html = re.sub(
    r"document\.getElementById\('aLangZh'\)\.classList\.toggle\('active', lang === 'zh'\);\s*document\.getElementById\('aLangEn'\)\.classList\.toggle\('active', lang === 'en'\);",
    r"const elZh = document.getElementById('aLangZh'); if(elZh) elZh.classList.toggle('active', lang === 'zh');\n  const elEn = document.getElementById('aLangEn'); if(elEn) elEn.classList.toggle('active', lang === 'en');",
    html
)

open('admin.html', 'w', encoding='utf-8').write(html)
print('Fixed admin lang crash')
