import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('window._events = data || [];', 'window._events = data.events || data || [];')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

with io.open('index.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('const events = await res.json();', 'const data = await res.json();\n    const events = data.events || data || [];')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text2)

print("Fixed parsing")
