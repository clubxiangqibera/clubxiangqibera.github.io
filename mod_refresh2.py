import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''<button class="btn" style="background:var(--green); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800; cursor:pointer;" onclick="document.getElementById('createGalleryModal').style.display='flex'">+ 创建新图集</button>'''

replacement = '''<div style="display:flex; gap:10px;">
  <button class="btn" style="background:var(--pri3); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800; cursor:pointer;" onclick="loadEvents(); if(typeof toast === 'function') toast('已刷新相册列表', 'info');">🔄 刷新列表</button>
  <button class="btn" style="background:var(--green); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800; cursor:pointer;" onclick="document.getElementById('createGalleryModal').style.display='flex'">+ 创建新图集</button>
</div>'''

text = text.replace(target, replacement)

empty_target = "container.innerHTML = '<div style=\"color:var(--text2);\">暂无活动图集，请在上方创建</div>';"
empty_replacement = "container.innerHTML = '<div style=\"color:var(--text2); padding:20px; text-align:center; width:100%; grid-column: 1 / -1;\">暂无活动图集，请在上方创建</div>';"

text = text.replace(empty_target, empty_replacement)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added refresh button and fixed empty state styling')
