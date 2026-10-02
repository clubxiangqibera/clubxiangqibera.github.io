import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="publicPodiumArea"')
print(text[max(0, idx):idx+1000].encode('ascii', 'ignore').decode('ascii'))
