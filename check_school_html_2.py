import io, re
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btnLangEn')
print(text[idx:idx+1500])
