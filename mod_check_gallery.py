import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('历届活动相册')
print(text[max(0, idx-200):idx+200].encode('ascii', 'ignore').decode('ascii'))
