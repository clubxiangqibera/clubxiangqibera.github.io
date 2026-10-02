import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# ========================================================
# 1. SHARED CSS TO INJECT INTO BOTH admin.html & school.html
# ========================================================
shared_css = '''
    /* FORCE DEEP NAVY + XIANGQI GRID BACKGROUND LIKE STUDENT LOGIN */
    body {
      background: #040C17 !important;
      color: #fff !important;
      min-height: 100vh;
      margin: 0;
      padding: 0;
      position: relative;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      z-index: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(241,196,15,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(241,196,15,0.04) 1px, transparent 1px);
      background-size: 72px 72px;
      mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 70%);
      -webkit-mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 70%);
    }

    /* TOP TAB BAR (NAVBAR) */
    .public-nav-bar {
      width: 100%; display: flex; justify-content: space-between; align-items: center;
      padding: 12px 24px; background: rgba(6, 23, 36, 0.92); backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08); position: sticky; top: 0; z-index: 9600;
      box-shadow: 0 2px 16px rgba(0, 0, 0, 0.4);
    }
    .p-nav-brand { display: flex; align-items: center; gap: 10px; text-decoration: none; }
    .p-nav-logo { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(241,196,15,0.4); }
    .p-nav-title { font-size: 16px; font-weight: 900; color: #fff; letter-spacing: -0.3px; }
    .p-nav-sub { font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.5); letter-spacing: 1.5px; text-transform: uppercase; }
    
    .nav-menu-btn {
      background: transparent; border: 1px solid rgba(255,255,255,0.15); color: #fff;
      padding: 6px 14px; border-radius: 18px; font-size: 13px; font-weight: 700;
      cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s;
    }
    .nav-menu-btn:hover { background: rgba(255,255,255,0.08); border-color: rgba(241,196,15,0.5); }

    /* APPLE MEGA MENU */
    .apple-mega-menu {
      position: fixed; top: 0; left: 0; width: 100%; z-index: 9500;
      background: rgba(6, 23, 36, 0.96); border-bottom: 1px solid rgba(255,255,255,0.08);
      transform: translateY(-100%); transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
      padding: 85px 30px 45px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    }
    .apple-mega-menu.open { transform: translateY(0); }
    .apple-mega-backdrop {
      position: fixed; inset: 0; z-index: 9400; background: rgba(0,0,0,0.6);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      opacity: 0; pointer-events: none; transition: opacity 0.4s ease;
    }
    .apple-mega-backdrop.open { opacity: 1; pointer-events: auto; }
    
    .apple-mega-container {
      max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 36px;
    }
    .apple-mega-col { display: flex; flex-direction: column; gap: 14px; }
    .apple-mega-col h4 {
      font-size: 13px; color: rgba(255,255,255,0.4); text-transform: uppercase;
      letter-spacing: 1.5px; margin-bottom: 6px; font-weight: 800; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;
    }
    .apple-mega-col a {
      color: #fff; font-size: 17px; font-weight: 700; text-decoration: none; cursor: pointer; transition: all 0.2s ease;
      display: flex; align-items: center;
    }
    .apple-mega-col a:hover { color: #F1C40F; transform: translateX(4px); }

    .apple-segment {
      display: flex; background: rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 4px; width: 100%; max-width: 280px;
    }
    .apple-segment .seg-btn {
      flex: 1; background: transparent; border: none; color: rgba(255, 255, 255, 0.5);
      padding: 8px 0; font-size: 13px; font-weight: 700; cursor: pointer; border-radius: 8px; transition: all 0.3s;
    }
    .apple-segment .seg-btn.active {
      background: rgba(255, 255, 255, 0.95); color: #111; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
'''

# ========================================================
# 2. SHARED NAVBAR + MEGA MENU HTML
# ========================================================
def get_nav_html(active_portal):
    admin_active_style = 'color:#F1C40F;' if active_portal == 'admin' else ''
    school_active_style = 'color:#F1C40F;' if active_portal == 'school' else ''
    return f'''
  <!-- PUBLIC STICKY TOP TAB BAR -->
  <header class="public-nav-bar">
    <a href="index.html" class="p-nav-brand">
      <img src="cxb_round_emblem.png" alt="CXB" class="p-nav-logo">
      <div>
        <div id="navBrandTitle" class="p-nav-title">百乐象棋俱乐部</div>
        <div class="p-nav-sub">CLUB XIANGQI BERA</div>
      </div>
    </a>
    <button class="nav-menu-btn" onclick="toggleMainNav()">
      <span id="navMenuBtnIcon">☰</span> <span id="navMenuBtnText">菜单</span>
    </button>
  </header>

  <!-- APPLE MEGA MENU & BACKDROP -->
  <div id="appleMegaBackdrop" class="apple-mega-backdrop" onclick="closeMainNav()"></div>
  <div id="appleMegaMenu" class="apple-mega-menu">
    <div class="apple-mega-container">
      
      <div class="apple-mega-col">
        <h4 id="menuExpTitle">探索俱乐部</h4>
        <a href="index.html" id="menuHomeLink">🏠 首页</a>
        <a href="index.html#ladder" id="menuLadderLink">🏆 天梯榜</a>
        <a href="index.html#events" id="menuEventsLink">📸 赛事与活动中心</a>
      </div>

      <div class="apple-mega-col">
        <h4 id="menuPortalsTitle">专属入口</h4>
        <a href="index.html#login" id="menuStudentLink">🔐 学员专属登录</a>
        <a href="school.html" id="menuSchoolLink" style="{school_active_style}">🏫 校际赛报名系统</a>
        <a href="admin.html" id="menuAdminLink" style="{admin_active_style}">👑 教练管理端</a>
      </div>

      <div class="apple-mega-col">
        <h4 id="menuLangTitle">系统语言</h4>
        <div class="apple-segment">
          <button type="button" class="seg-btn" id="mSegZh" onclick="changeGlobalLang('zh')">中文</button>
          <button type="button" class="seg-btn" id="mSegBm" onclick="changeGlobalLang('bm')">Melayu</button>
          <button type="button" class="seg-btn" id="mSegEn" onclick="changeGlobalLang('en')">English</button>
        </div>
      </div>

    </div>
  </div>
'''

# ========================================================
# 3. SHARED JAVASCRIPT FOR NAVBAR & LANGUAGE
# ========================================================
shared_js = '''
function toggleMainNav() {
  const menu = document.getElementById('appleMegaMenu');
  const backdrop = document.getElementById('appleMegaBackdrop');
  const btnText = document.getElementById('navMenuBtnText');
  const btnIcon = document.getElementById('navMenuBtnIcon');
  if(!menu) return;

  if(menu.classList.contains('open')) {
    closeMainNav();
  } else {
    menu.classList.add('open');
    backdrop.classList.add('open');
    if(btnText) btnText.innerText = (window._currentLang === 'en' ? 'Close' : (window._currentLang === 'bm' ? 'Tutup' : '关闭'));
    if(btnIcon) btnIcon.innerText = '✕';
  }
}

function closeMainNav() {
  const menu = document.getElementById('appleMegaMenu');
  const backdrop = document.getElementById('appleMegaBackdrop');
  if(menu) menu.classList.remove('open');
  if(backdrop) backdrop.classList.remove('open');
  
  const btnText = document.getElementById('navMenuBtnText');
  const btnIcon = document.getElementById('navMenuBtnIcon');
  if(btnText) btnText.innerText = (window._currentLang === 'en' ? 'Menu' : (window._currentLang === 'bm' ? 'Menu' : '菜单'));
  if(btnIcon) btnIcon.innerText = '☰';
}
'''

print("Templates ready.")
