import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Script block to insert right before </body>
nav_script = '''
<script>
// ==========================================
// Apple Mega Menu & Top Nav Controller
// ==========================================
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
    if(backdrop) backdrop.classList.add('open');
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

function changeGlobalLang(lang) {
  if(typeof setAdminLang === 'function') setAdminLang(lang);
  if(typeof setLoginLang === 'function') setLoginLang(lang);
  updateMenuI18n(lang);
}

function updateMenuI18n(lang) {
  window._currentLang = lang;
  try { localStorage.setItem('cxb_lang_pref', lang); } catch(e){}
  
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

  const isOpen = document.getElementById('appleMegaMenu') && document.getElementById('appleMegaMenu').classList.contains('open');

  if(lang === 'zh') {
    if(btnText && !isOpen) btnText.innerText = '菜单';
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
    if(btnText && !isOpen) btnText.innerText = 'Menu';
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
    if(btnText && !isOpen) btnText.innerText = 'Menu';
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

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('cxb_lang_pref') || 'zh';
  changeGlobalLang(saved);
});
</script>
'''

for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. ELIMINATE PADDING ON #loginScreen and #schoolLoginScreen
    content = re.sub(r'#loginScreen\s*\{[^}]*\}', '#loginScreen { min-height: 100vh; display: flex; flex-direction: column; padding: 0 !important; margin: 0 !important; background: transparent; width: 100% !important; }', content)
    content = re.sub(r'#schoolLoginScreen\s*\{[^}]*\}', '#schoolLoginScreen { min-height: 100vh; display: flex; flex-direction: column; padding: 0 !important; margin: 0 !important; background: transparent; width: 100% !important; }', content)

    # 2. ENSURE .public-nav-bar has 0 margin, 100% width, top: 0
    content = content.replace('.public-nav-bar {', '.public-nav-bar { margin: 0 !important; top: 0 !important; left: 0 !important; width: 100% !important; ')

    # 3. Ensure body has 0 margin/padding
    content = re.sub(r'body\s*\{[^}]*\}', 'body { margin: 0 !important; padding: 0 !important; font-family: "Plus Jakarta Sans", "Noto Sans SC", sans-serif; background: #040C17 !important; color: #fff; min-height: 100vh; -webkit-font-smoothing: antialiased; }', content, count=1)

    # 4. Inject nav_script before </body>
    if 'function toggleMainNav' not in content:
        # Find </body> and insert right before it
        idx_body = content.rfind('</body>')
        if idx_body != -1:
            content = content[:idx_body] + nav_script + '\n' + content[idx_body:]
        else:
            content = content + nav_script

    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file} updated successfully!")

print("All done.")
