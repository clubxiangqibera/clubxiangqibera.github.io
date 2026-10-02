import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Top Nav HTML
old_nav = re.search(r'<nav class="p-nav">.*?</nav>', text, flags=re.DOTALL)
if old_nav:
    new_nav = '''<nav class="p-nav">
    <div class="p-nav-brand">
      <img src="cxb_round_emblem.png" alt="CXBLogo">
      <div>
        <div style="font-size:16px; font-weight:900; color:#fff; letter-spacing:-0.3px;" data-i18n="hero.title">百乐象棋俱乐部</div>
        <div style="font-size:10px; font-weight:700; color:var(--gold-soft); letter-spacing:1.5px;">CLUB XIANGQI BERA</div>
      </div>
    </div>
    <button class="btn btn--primary" style="padding: 10px 18px; font-size: 14px; display:flex; gap:8px; align-items:center;" onclick="openMainNav()">
      <span>☰</span> 菜单
    </button>
  </nav>'''
    text = text.replace(old_nav.group(0), new_nav)
else:
    print("Could not find <nav class='p-nav'>")

# 2. Inject CSS for Drawer Buttons
css = '''
.nav-drawer-btn {
  width: 100%; text-align: left; padding: 16px 20px;
  background: transparent; border: 1px solid var(--line);
  border-radius: var(--radius); color: var(--ink);
  font-size: 1.1rem; font-weight: 700; font-family: var(--font-serif);
  cursor: pointer; transition: 0.2s; text-decoration: none; display: block;
}
.nav-drawer-btn:hover {
  background: var(--navy-800); border-color: var(--gold); color: var(--gold);
  transform: translateX(6px);
}
#mainNavSidebar { z-index: 9500; }
#mainNavBackdrop { z-index: 9400; }
'''
text = text.replace('</style>', css + '\n</style>')

# 3. Inject HTML for Main Nav Sidebar
main_nav_html = '''
<!-- === MAIN NAV SIDEBAR === -->
<div id="mainNavBackdrop" class="archive-backdrop" onclick="closeMainNav()"></div>
<div id="mainNavSidebar" class="archive-view" style="width: 340px;">
  <div class="archive-view__header">
    <div class="archive-view__title">🧭 导航 (Navigation)</div>
    <button class="archive-view__close" onclick="closeMainNav()">×</button>
  </div>
  <div class="archive-view__body" style="padding: 24px; display: flex; flex-direction: column; gap: 12px;">
    
    <button class="nav-drawer-btn" onclick="togglePublicTab('home'); closeMainNav()" data-i18n="nav.home">🏠 首页</button>
    <button class="nav-drawer-btn" onclick="togglePublicTab('ladder'); closeMainNav()" data-i18n="nav.ladder">🏆 天梯榜</button>
    <button class="nav-drawer-btn" onclick="openArchiveView(); closeMainNav()" data-i18n="events.title">📸 赛事与活动中心</button>
    <button class="nav-drawer-btn" onclick="togglePublicTab('login'); closeMainNav()" data-i18n="nav.login">🔐 学员登录</button>
    
    <div style="height: 1px; background: var(--line); margin: 12px 0;"></div>
    
    <a href="school.html" class="nav-drawer-btn" style="color: var(--silver);">🏫 校际赛入口 (Schools)</a>
    <a href="admin.html" class="nav-drawer-btn" style="color: var(--gold);">👑 教练管理端 (Admin)</a>

    <div style="height: 1px; background: var(--line); margin: 12px 0;"></div>
    
    <div style="font-size: 13px; font-weight:700; color: var(--ink-dim); margin-bottom: 8px;">🌐 语言 / Language</div>
    <div class="lang" style="display: flex; gap: 8px;">
      <button onclick="setLang('cn', this); closeMainNav()" class="btn btn--ghost" style="flex:1; padding:10px; font-size:13px;" aria-pressed="true">中文</button>
      <button onclick="setLang('bm', this); closeMainNav()" class="btn btn--ghost" style="flex:1; padding:10px; font-size:13px;">BM</button>
      <button onclick="setLang('en', this); closeMainNav()" class="btn btn--ghost" style="flex:1; padding:10px; font-size:13px;">EN</button>
    </div>

  </div>
</div>
'''
text = text.replace('</body>', main_nav_html + '\n</body>')

# 4. Inject JS
js = '''
function openMainNav() {
  document.getElementById('mainNavSidebar').classList.add('open');
  document.getElementById('mainNavBackdrop').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMainNav() {
  document.getElementById('mainNavSidebar').classList.remove('open');
  document.getElementById('mainNavBackdrop').classList.remove('open');
  document.body.style.overflow = '';
}
'''
text = text.replace('// --- END SUPER EVENT SYSTEM ---', '// --- END SUPER EVENT SYSTEM ---\n' + js)

# Remove the old floating language picker since it's now in the sidebar menu!
old_lang = re.search(r'<div class="lang" style="position:fixed; bottom:20px; right:20px; z-index:100;.*?</div>', text, flags=re.DOTALL)
if old_lang:
    text = text.replace(old_lang.group(0), '')
else:
    # Try finding it in case the style is slightly different
    old_lang = re.search(r'<div class="lang".*?</button>\s*</div>', text, flags=re.DOTALL)
    if old_lang and 'fixed' in old_lang.group(0):
        text = text.replace(old_lang.group(0), '')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Complete Nav Rework Applied.")
