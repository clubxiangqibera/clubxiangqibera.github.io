import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('publicLoginSection')
while idx != -1:
    print(text[max(0, idx-100):idx+200])
    idx = text.find('publicLoginSection', idx+1)
