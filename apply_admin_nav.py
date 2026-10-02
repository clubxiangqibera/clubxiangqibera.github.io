import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from build_templates import shared_css, get_nav_html, shared_js

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
text = text.replace('</style>', shared_css + '\n</style>')

# 2. Build the new admin #loginScreen HTML
new_login_screen = f'''
<div id="loginScreen" style="min-height:100vh; display:flex; flex-direction:column; background:transparent; position:relative; z-index:1;">
  {get_nav_html('admin')}

  <!-- CENTER LOGIN CARD (EXACTLY MATCHING STUDENT LOGIN) -->
  <div style="flex:1; display:flex; justify-content:center; align-items:center; padding:30px 20px;">
    <div class="gate-card animate-zoom" style="margin:0 auto; width:100%; max-width:440px; background:rgba(6, 23, 36, 0.95); padding:40px; border-radius:24px; box-shadow:0 20px 50px rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); text-align:center;">
      
      <div id="aBadge" style="display:inline-block; background:#F1C40F; color:#0A1929; padding:6px 14px; border-radius:30px; font-size:12px; font-weight:800; margin-bottom:20px;">👑 CLUB XIANGQI BERA · 教练管理端</div>
      <h1 id="aTitle" style="font-family:'Noto Serif SC', serif; font-size:26px; color:#fff; margin-bottom:8px; font-weight:900;">百乐象棋俱乐部</h1>
      <p class="sub" id="aSub" style="font-size:14px; color:rgba(255,255,255,0.6); margin-bottom:32px;">请使用俱乐部发放的教练密码登入控制台</p>

      <form onsubmit="event.preventDefault(); tryLogin(); return false;">
        <div class="login-input-wrap" style="text-align:left; margin-bottom:32px;">
          <label id="aLbl" style="display:block; font-size:13px; font-weight:700; color:rgba(255,255,255,0.6); margin-bottom:8px;">🔑 管理密码 (Admin Password)</label>
          <input type="password" id="adminPinInput" class="pin-input" placeholder="请输入密码" maxlength="16" autofocus autocomplete="current-password" style="width:100%; padding:14px 16px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:10px; color:#fff; font-size:15px; outline:none; text-align:left;">
        </div>
        
        <button type="submit" class="login-btn" id="aBtn" style="width:100%; padding:16px; background:linear-gradient(135deg, #E63946 0%, #D90429 100%); color:#fff; font-size:16px; font-weight:700; border:none; border-radius:10px; cursor:pointer; box-shadow:0 4px 15px rgba(217,4,41,0.3); transition:transform 0.2s;">🚨 登录进入系统</button>
      </form>
      
      <div class="login-error" id="loginError" style="margin-top:16px; display:none; color:#E63946; font-size:13px; font-weight:700;">❌ 密码错误，请重新输入 (Invalid Password)</div>
    </div>
  </div>
</div>
'''

# Replace the entire old <div id="loginScreen">...</div>
old_login_screen_match = re.search(r'<div id="loginScreen">.*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if old_login_screen_match:
    text = text.replace(old_login_screen_match.group(0), new_login_screen)
else:
    # fallback: replace up to adminApp
    idx_login = text.find('<div id="loginScreen">')
    idx_app = text.find('<div id="adminApp"')
    text = text[:idx_login] + new_login_screen + '\n' + text[idx_app:]

# 3. Add changeGlobalLang and nav JS to admin.html
admin_lang_js = shared_js + '''
function changeGlobalLang(lang) {
  setAdminLang(lang);
}

function updateMenuI18n(lang) {
  window._currentLang = lang;
  const segZh = document.getElementById('mSegZh');
  const segBm = document.getElementById('mSegBm');
  const segEn = document.getElementById('mSegEn');
  if(segZh) segZh.className = 'seg-btn' + (lang === 'zh' ? ' active' : '');
  if(segBm) segBm.className = 'seg-btn' + (lang === 'bm' ? ' active' : '');
  if(segEn) segEn.className = 'seg-btn' + (lang === 'en' ? ' active' : '');

  const btnText = document.getElementById('navMenuBtnText');
  const expTitle = document.getElementById('menuExpTitle');
  const portalsTitle = document.getElementById('menuPortalsTitle');
  const langTitle = document.getElementById('menuLangTitle');
  const homeLink = document.getElementById('menuHomeLink');
  const ladderLink = document.getElementById('menuLadderLink');
  const eventsLink = document.getElementById('menuEventsLink');
  const studentLink = document.getElementById('menuStudentLink');
  const schoolLink = document.getElementById('menuSchoolLink');
  const adminLink = document.getElementById('menuAdminLink');

  if(lang === 'zh') {
    if(btnText) btnText.innerText = '菜单';
    if(expTitle) expTitle.innerText = '探索俱乐部';
    if(portalsTitle) portalsTitle.innerText = '专属入口';
    if(langTitle) langTitle.innerText = '系统语言';
    if(homeLink) homeLink.innerText = '🏠 首页';
    if(ladderLink) ladderLink.innerText = '🏆 天梯榜';
    if(eventsLink) eventsLink.innerText = '📸 赛事与活动中心';
    if(studentLink) studentLink.innerText = '🔐 学员专属登录';
    if(schoolLink) schoolLink.innerText = '🏫 校际赛报名系统';
    if(adminLink) adminLink.innerText = '👑 教练管理端';
  } else if(lang === 'bm') {
    if(btnText) btnText.innerText = 'Menu';
    if(expTitle) expTitle.innerText = 'Terokai Kelab';
    if(portalsTitle) portalsTitle.innerText = 'Portal Khas';
    if(langTitle) langTitle.innerText = 'Bahasa Sistem';
    if(homeLink) homeLink.innerText = '🏠 Utama';
    if(ladderLink) ladderLink.innerText = '🏆 Kedudukan';
    if(eventsLink) eventsLink.innerText = '📸 Pusat Acara & Aktiviti';
    if(studentLink) studentLink.innerText = '🔐 Log Masuk Pelajar';
    if(schoolLink) schoolLink.innerText = '🏫 Sistem Antara Sekolah';
    if(adminLink) adminLink.innerText = '👑 Portal Jurulatih';
  } else {
    if(btnText) btnText.innerText = 'Menu';
    if(expTitle) expTitle.innerText = 'Explore Club';
    if(portalsTitle) portalsTitle.innerText = 'Portals';
    if(langTitle) langTitle.innerText = 'System Language';
    if(homeLink) homeLink.innerText = '🏠 Home';
    if(ladderLink) ladderLink.innerText = '🏆 Ladder';
    if(eventsLink) eventsLink.innerText = '📸 Events & Activities';
    if(studentLink) studentLink.innerText = '🔐 Student Login';
    if(schoolLink) schoolLink.innerText = '🏫 Schools Portal';
    if(adminLink) adminLink.innerText = '👑 Admin Portal';
  }
}

// Hook setAdminLang to also call updateMenuI18n
const origSetAdminLang = setAdminLang;
setAdminLang = function(lang) {
  origSetAdminLang(lang);
  updateMenuI18n(lang);
};
'''

text = text.replace('</script>\n</body>', admin_lang_js + '\n</script>\n</body>')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("admin.html fully upgraded!")
