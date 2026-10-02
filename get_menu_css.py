import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('.apple-mega-menu')
idx2 = text.find('</style>', idx1)
print(text[idx1:idx2])
