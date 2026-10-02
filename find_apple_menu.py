import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('appleMegaMenu')
while idx != -1:
    print('Found at', idx)
    print(text[max(0, idx-50):idx+400])
    idx = text.find('appleMegaMenu', idx+1)
