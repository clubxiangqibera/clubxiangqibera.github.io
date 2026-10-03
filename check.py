import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
html = open('school.html', encoding='utf-8').read()
idx = html.find('function setLoginLang')
print(html[idx:idx+800])
