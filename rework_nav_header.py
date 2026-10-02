import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Top Nav HTML
old_nav = re.search(r'<header class="public-nav-bar">.*?</header>', text, flags=re.DOTALL)
if old_nav:
    new_nav = '''<header class="public-nav-bar">
    <div class="p-nav-brand">
      <img src="cxb_round_emblem.png" alt="CXB" class="p-nav-logo">
      <div>
        <div class="p-nav-title" data-i18n="hero.title">百乐象棋俱乐部</div>
        <div class="p-nav-sub">CLUB XIANGQI BERA</div>
      </div>
    </div>
    <button class="btn btn--primary" style="padding: 10px 18px; font-size: 14px; display:flex; gap:8px; align-items:center;" onclick="openMainNav()">
      <span>☰</span> <span data-i18n="nav.menu">菜单</span>
    </button>
  </header>'''
    text = text.replace(old_nav.group(0), new_nav)
    print("Replaced public-nav-bar successfully.")
else:
    print("Could not find public-nav-bar")

# 2. Add translation for nav.menu if missing
if '"nav.menu"' not in text:
    text = text.replace('"nav.login": "登录",', '"nav.login": "登录",\n    "nav.menu": "菜单",')
    text = text.replace('"nav.login": "Log Masuk",', '"nav.login": "Log Masuk",\n    "nav.menu": "Menu",')
    text = text.replace('"nav.login": "Login",', '"nav.login": "Login",\n    "nav.menu": "Menu",')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Complete Nav Rework Applied.")
