import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<div class="nav-tab superadmin-only" data-tab="licenses"'
replacement = '<div class="nav-tab superadmin-only" data-tab="gallery" onclick="switchTab(\'gallery\')">📸 活动相册</div>\n    ' + target

text = text.replace(target, replacement)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Tab injected!")
