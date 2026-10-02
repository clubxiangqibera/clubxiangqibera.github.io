import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('publicLadderSection')
print(text[max(0, idx-50):idx+300])
