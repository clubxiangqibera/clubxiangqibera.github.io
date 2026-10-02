import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="loginScreen"')
print(text[idx1-200:idx1+1000])
