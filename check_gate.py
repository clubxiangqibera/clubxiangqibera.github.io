import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="gate-card"')
if idx != -1:
    print(text[max(0, idx-300):idx+300])
else:
    print('HTML gate-card not found')
