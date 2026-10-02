import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add the button to the navbar
old_nav = r'<button class="p-nav-btn" id="tabBtnLadder" onclick="togglePublicTab\(\'ladder\'\)">🏆 天梯榜</button>'
new_nav = '''<button class="p-nav-btn" id="tabBtnLadder" onclick="togglePublicTab('ladder')">🏆 天梯榜</button>
      <button class="p-nav-btn" id="tabBtnEvents" onclick="openArchiveView()">📸 活动中心</button>'''
      
text = re.sub(old_nav, new_nav, text)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Added to nav.")
