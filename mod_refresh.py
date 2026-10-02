import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<button class="btn" style="padding:8px 16px; background:var(--green); color:#fff; border:none; border-radius:10px; font-weight:800;" onclick="showCreateModal()">+ 创建新相册</button>'
replacement = '''<div style="display:flex; gap:10px;">
  <button class="btn" style="padding:8px 16px; background:var(--pri3); color:#fff; border:none; border-radius:10px; font-weight:800;" onclick="loadEvents(); if(typeof toast === 'function') toast('已刷新相册', 'info');">🔄 刷新</button>
  <button class="btn" style="padding:8px 16px; background:var(--green); color:#fff; border:none; border-radius:10px; font-weight:800;" onclick="showCreateModal()">+ 创建新相册</button>
</div>'''

if target in text:
    text = text.replace(target, replacement)
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added refresh button.")
else:
    print("Target not found.")
