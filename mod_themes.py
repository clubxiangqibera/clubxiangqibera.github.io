import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean up #securityGate
clean_sg = """#securityGate {
      display: flex; flex-direction: column; align-items: center;
      width: 100%; min-height: 100vh; padding: 0;
    }"""
text = re.sub(r'#securityGate\s*\{[^}]*\}', clean_sg, text)

# 2. Remove the backdrop-filter stuff I added for cards
text = re.sub(r'#securityGate \.pod,[^{]*\{\s*backdrop-filter:[^}]*\}', '', text)

# 3. Update Light Mode background to Light Blue
# Current: --bg: #F0F4F8;
# New: --bg: #E1EDF7; (Very nice soft light blue)
text = text.replace('--bg: #F0F4F8;', '--bg: #E3F0FA;')
text = text.replace('--border: #E8ECF0;', '--border: #D0E1F0;')

# 4. Update Dark Mode background to Deep Midnight Blue
# Current: --bg:#0B0F14;
# New: --bg: #030C16;
text = text.replace('--bg:#0B0F14;', '--bg:#030B14;')
# Dark mode card from #141A23 to slightly blue tinted dark
text = text.replace('--card:#141A23;', '--card:#0C1A29;')
text = text.replace('--border:#263242;', '--border:#162C45;')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Also apply to admin.html and school.html ?
# Wait, admin.html also has these CSS vars. Let's update them too so it's consistent.
for file_name in ['admin.html']:
    try:
        with io.open(file_name, 'r', encoding='utf-8') as f:
            text2 = f.read()
        text2 = text2.replace('--bg: #F0F4F8;', '--bg: #E3F0FA;')
        text2 = text2.replace('--border: #E8ECF0;', '--border: #D0E1F0;')
        text2 = text2.replace('--bg:#0B0F14;', '--bg:#030B14;')
        text2 = text2.replace('--card:#141A23;', '--card:#0C1A29;')
        text2 = text2.replace('--border:#263242;', '--border:#162C45;')
        with io.open(file_name, 'w', encoding='utf-8') as f:
            f.write(text2)
    except:
        pass

print("Themes updated!")
