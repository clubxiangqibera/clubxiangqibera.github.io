import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('admin_lang_js in admin.html?', 'function toggleMainNav' in text)
print('End of file:')
print(text[-500:])
