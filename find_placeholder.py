import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('placeholder')
while idx != -1:
    print(text[max(0, idx-50):idx+100])
    idx = text.find('placeholder', idx+1)
