import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('admin_lang_js in school.html?', 'function toggleMainNav' in text)
