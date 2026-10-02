import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

empty_target = "container.innerHTML = '<div style=\"color:var(--text2);\">暂无活动相册，点击上方新建。</div>';"
empty_replacement = "container.innerHTML = '<div style=\"color:var(--text2); padding:40px; text-align:center; width:100%; grid-column: 1 / -1;\">暂无活动相册，点击上方新建。</div>';"

if empty_target in text:
    text = text.replace(empty_target, empty_replacement)
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed empty state styling!")
else:
    print("Target not found.")
