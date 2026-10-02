import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update :root
root_css = """:root {
      --primary: #0E2F44;
      --primary-mid: #1A5276;
      --primary-light: #2980B9;
      --gold: #F39C12;
      --gold-glow: rgba(243,156,18,0.35);
      --silver: #95A5A6;
      --bronze: #D35400;
      --bg: #E3F0FA;
      --card: #FFFFFF;
      --text: #1C2833;
      --text2: #6B7B8D;
      --border: #D0E1F0;
      --green: #27AE60;
      --red: #E74C3C;
      --radius: 20px;
      --shadow: 0 6px 24px rgba(0,0,0,0.07);
      
      --hero-bg: linear-gradient(145deg, #071A27 0%, #0E2F44 55%, #1A5276 100%);
      --hero-border: none;
      --glass-blur: none;
    }
    @media(prefers-color-scheme:dark){
      :root{
        --bg: linear-gradient(145deg, #04101A 0%, #0A2238 50%, #103A5E 100%);
        --card: rgba(255, 255, 255, 0.05);
        --text: #F0F4F8;
        --text2: #9CA8B7;
        --border: rgba(255, 255, 255, 0.1);
        --shadow: 0 8px 30px rgba(0,0,0,0.4);
        
        --hero-bg: rgba(0, 0, 0, 0.35);
        --hero-border: 1px solid rgba(255,255,255,0.08);
        --glass-blur: blur(16px);
      }
    }"""

# Replace root section
text = re.sub(r':root\s*\{.*?\@media\(prefers-color-scheme:dark\)\{\s*:root\{.*?\}\s*\}', root_css, text, flags=re.DOTALL)

# 2. Update body background-attachment
text = text.replace('background:var(--bg);color:var(--text);', 'background:var(--bg);color:var(--text);background-attachment:fixed;')

# 3. Update .public-hero
# Find .public-hero and replace its background
def replace_hero(match):
    return """.public-hero {
      width: 100%;
      background: var(--hero-bg);
      border: var(--hero-border);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);"""

text = re.sub(r'\.public-hero\s*\{\s*width:\s*100%;\s*background:\s*linear-gradient\([^)]+\);', replace_hero, text)

# Also need to add backdrop-filter to cards in general to make --card: rgba work
# Wait, I can just add backdrop-filter to .gate-card, .pod, .rank-item, .vip-invite-card
# We can add a generic rule:
generic_glass = """
    .gate-card, .pod, .rank-item, .vip-invite-card {
       backdrop-filter: var(--glass-blur);
       -webkit-backdrop-filter: var(--glass-blur);
    }
    """
text = text.replace('/* ========================================================', generic_glass + '\n    /* ========================================================')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Do the same for admin.html
try:
    with io.open('admin.html', 'r', encoding='utf-8') as f:
        text2 = f.read()
    text2 = re.sub(r':root\s*\{.*?\@media\(prefers-color-scheme:dark\)\{\s*:root\{.*?\}\s*\}', root_css, text2, flags=re.DOTALL)
    text2 = text2.replace('background:var(--bg);color:var(--text);', 'background:var(--bg);color:var(--text);background-attachment:fixed;')
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text2)
except:
    pass

print('Updated theme completely')
