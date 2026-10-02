import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update #securityGate CSS
new_sg_css = """#securityGate {
      display: flex; flex-direction: column; align-items: center;
      width: 100%; min-height: 100vh; padding: 0;
      background: linear-gradient(145deg, #061724 0%, #0E2F44 45%, #1A5276 100%);
      color: #fff;
      --bg: transparent; 
      --card: rgba(255, 255, 255, 0.08); 
      --text: #FFFFFF;
      --text2: #A0B3C2;
      --border: rgba(255, 255, 255, 0.12);
      --shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    #securityGate .pod,
    #securityGate .gate-card,
    #securityGate .vip-invite-card,
    #securityGate .rank-item {
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }"""

text = re.sub(r'#securityGate\s*\{\s*display:\s*flex;[^}]*\}', new_sg_css, text)

# Just in case my regex missed it because I removed some stuff earlier
if new_sg_css not in text:
    # Look for the current #securityGate
    text = re.sub(r'#securityGate\s*\{.*?\}', new_sg_css, text, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
