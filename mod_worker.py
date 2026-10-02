import io

with io.open('../worker_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_loop = 'for (const k of listRes.keys) {'
new_loop = 'for (const k of listRes.keys) {\n          if (!k.name.startsWith("CXB-")) continue;'

if old_loop in text and 'k.name.startsWith' not in text:
    text = text.replace(old_loop, new_loop)
    with io.open('../worker_v2.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 2: Fixed worker_v2.js')
