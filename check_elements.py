import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('renderPublicLadder(players)')
print('Ladder:', idx)
if idx != -1: print(text[idx:idx+200])

idx = text.find('gate-card')
print('Gate:', idx)
if idx != -1: print(text[idx-50:idx+200])

idx = text.find('const i18n = {')
print('i18n:', idx)
if idx != -1: print(text[idx:idx+200])
