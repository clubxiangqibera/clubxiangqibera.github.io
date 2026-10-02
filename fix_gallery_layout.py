import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure publicGalleryArea is block/full width and the empty class is defined
css_fixes = '''
#publicGalleryArea { width: 100%; display: block; margin-top: 20px; }
.empty {
  width: 100%;
  padding: 36px 20px; text-align: center;
  color: var(--ink-dim);
  border: 1px dashed var(--line);
  border-radius: var(--radius);
  margin: 0 auto;
}
'''
text = text.replace('</style>', css_fixes + '\n</style>')

# Ensure HTML has the empty class
old_html = r'<div id="publicGalleryArea">\s*<div[^>]*>暂无公开相册。</div>\s*</div>'
new_html = '''<div id="publicGalleryArea">
          <div class="empty" data-i18n="gallery.empty">暂无公开相册。</div>
        </div>'''
text = re.sub(old_html, new_html, text)

# Ensure the JS loadPublicEvents doesn't override with inline styles that break it
old_js_empty = r"container\.innerHTML = '<div style=\"color:var\(--text2\); font-size:13px;\">暂无公开相册。</div>';"
new_js_empty = "container.innerHTML = '<div class=\"empty\" data-i18n=\"gallery.empty\">暂无公开相册。</div>';"
text = re.sub(old_js_empty, new_js_empty, text)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Gallery empty state fixed.")
