import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "prog.style.display = 'none';\n}"
end_marker = "function compressImage(file) {"

start_idx = text.find(start_marker)
if start_idx != -1:
    start_idx += len(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
    text = text[:start_idx] + '\n\n' + text[end_idx:]
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Garbage cleanly removed.')
else:
    print('Markers not found.')
