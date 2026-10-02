import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the Navbar Button to have IDs for toggling text
old_nav = r'<button class="nav-menu-btn" onclick="openMainNav\(\)">\s*<span>☰</span> <span data-i18n="nav.menu">菜单</span>\s*</button>'
new_nav = '''<button class="nav-menu-btn" onclick="toggleMainNav()">
      <span id="navMenuBtnIcon" style="font-size:16px;">☰</span> <span id="navMenuBtnText" data-i18n="nav.menu">菜单</span>
    </button>'''
text = re.sub(old_nav, new_nav, text)

# Also ensure the public-nav-bar has a very high z-index so it sits above the mega menu
text = text.replace('class="public-nav-bar"', 'class="public-nav-bar" style="position:relative; z-index:9600;"')

# 2. Remove the old right-side drawer HTML
old_drawer = re.search(r'<!-- === MAIN NAV SIDEBAR === -->.*?</div>\s*</div>', text, flags=re.DOTALL)
if old_drawer:
    text = text.replace(old_drawer.group(0), '')

# 3. Inject Apple-style Mega Menu HTML
mega_menu_html = '''
<!-- === APPLE STYLE MEGA MENU === -->
<div id="appleMegaBackdrop" class="apple-backdrop" onclick="closeMainNav()"></div>
<div id="appleMegaMenu" class="apple-mega-menu">
  <div class="apple-mega-container">
    
    <div class="apple-mega-col">
      <h4>探索俱乐部 (Explore)</h4>
      <a onclick="togglePublicTab('home'); closeMainNav()">首页 (Home)</a>
      <a onclick="togglePublicTab('ladder'); closeMainNav()">天梯榜 (Leaderboard)</a>
      <a onclick="openArchiveView(); closeMainNav()">赛事与活动中心 (Events)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4>专属入口 (Portals)</h4>
      <a onclick="togglePublicTab('login'); closeMainNav()">学员专属登录 (Student Login)</a>
      <a href="school.html">校际赛报名系统 (Schools)</a>
      <a href="admin.html">教练管理端 (Admin)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4>系统语言 (Language)</h4>
      <a onclick="setLang('cn'); closeMainNav()">中文 (Chinese)</a>
      <a onclick="setLang('bm'); closeMainNav()">Bahasa Melayu (BM)</a>
      <a onclick="setLang('en'); closeMainNav()">English (EN)</a>
    </div>

  </div>
</div>
'''
text = text.replace('</body>', mega_menu_html + '\n</body>')

# 4. Inject Mega Menu CSS
mega_css = '''
.apple-backdrop {
  position: fixed; inset: 0; z-index: 9400;
  background: rgba(4, 12, 23, 0.5);
  backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
  opacity: 0; pointer-events: none; transition: opacity 0.5s ease;
}
.apple-backdrop.open { opacity: 1; pointer-events: auto; }

.apple-mega-menu {
  position: fixed; top: 0; left: 0; width: 100%; z-index: 9500;
  background: rgba(6, 23, 36, 0.95); /* Deep navy translucent */
  border-bottom: 1px solid rgba(255,255,255,0.08);
  transform: translateY(-100%);
  transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
  padding: 100px 40px 60px; /* Extra top padding to clear navbar */
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.apple-mega-menu.open { transform: translateY(0); }

.apple-mega-container {
  max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 40px;
}
.apple-mega-col { display: flex; flex-direction: column; gap: 16px; }
.apple-mega-col h4 {
  font-size: 13px; color: rgba(255,255,255,0.4); text-transform: uppercase;
  letter-spacing: 1.5px; margin-bottom: 8px; font-weight: 800; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px;
}
.apple-mega-col a {
  color: #fff; font-size: 18px; font-weight: 700; text-decoration: none;
  cursor: pointer; transition: all 0.3s ease; font-family: var(--font-serif);
  display: flex; align-items: center;
}
.apple-mega-col a:hover { color: var(--gold); transform: translateX(4px); }
'''
text = text.replace('</style>', mega_css + '\n</style>')

# 5. Replace Old JS with New Toggle JS
old_js = re.search(r'// --- MAIN NAV SYSTEM ---.*?// --- END MAIN NAV SYSTEM ---', text, flags=re.DOTALL)
new_js = '''// --- MAIN NAV SYSTEM ---
function toggleMainNav() {
  const menu = document.getElementById('appleMegaMenu');
  const backdrop = document.getElementById('appleMegaBackdrop');
  const btnText = document.getElementById('navMenuBtnText');
  const btnIcon = document.getElementById('navMenuBtnIcon');

  if(menu.classList.contains('open')) {
    closeMainNav();
  } else {
    menu.classList.add('open');
    backdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
    if(btnText) btnText.innerText = '关闭';
    if(btnIcon) btnIcon.innerText = '✕';
  }
}
function closeMainNav() {
  const menu = document.getElementById('appleMegaMenu');
  const backdrop = document.getElementById('appleMegaBackdrop');
  if(menu) menu.classList.remove('open');
  if(backdrop) backdrop.classList.remove('open');
  document.body.style.overflow = '';
  
  const btnText = document.getElementById('navMenuBtnText');
  const btnIcon = document.getElementById('navMenuBtnIcon');
  if(btnText) btnText.innerText = '菜单';
  if(btnIcon) btnIcon.innerText = '☰';
}
// --- END MAIN NAV SYSTEM ---'''

if old_js:
    text = text.replace(old_js.group(0), new_js)
else:
    # If not found, inject it
    text = text.replace('</script>\n</body>', new_js + '\n</script>\n</body>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Apple Mega Menu Applied.")
