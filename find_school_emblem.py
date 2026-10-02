import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('cxb-emblem')
while idx != -1:
    print('Found at', idx)
    print(text[max(0, idx-100):idx+300])
    idx = text.find('cxb-emblem', idx+1)
