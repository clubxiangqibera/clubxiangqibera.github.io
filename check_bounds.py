import io, sys, re
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s = text.find('<div id="securityGate">')
e = text.find('<div id="authenticatedApp"', s)
print('e (authenticatedApp):', e)

# The end of securityGate is the </div> just before authenticatedApp.
print(text[e-100:e])
