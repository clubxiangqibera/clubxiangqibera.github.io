import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the header for the full list
header_pattern = r'<div class="section-head" style="margin-top:36px;">\s*<div class="section-title">📋 现役学员总榜[\s\S]*?</div>\s*</div>'
text = re.sub(header_pattern, '', text)

# 2. Modify renderPublicLadder to slice from index 3
old_js = '''const list = document.getElementById('publicRankList');
  if (list && p.length) {
    list.innerHTML = p.map((pl, i) => {'''

new_js = '''const list = document.getElementById('publicRankList');
  if (list && p.length > 3) {
    list.innerHTML = p.slice(3).map((pl, i) => {
      const realIndex = i + 3;'''

text = text.replace(old_js, new_js)

# And change the rank-num to use realIndex
text = text.replace('<div class="rank-num">${i + 1}</div>', '<div class="rank-num">${typeof realIndex !== "undefined" ? realIndex + 1 : i + 1}</div>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done modifying index.html')
