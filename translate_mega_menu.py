import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add data-i18n to Mega Menu
mega_old = r'''<div class="apple-mega-col">
      <h4>探索俱乐部 \(Explore\)</h4>
      <a onclick="togglePublicTab\('home'\); closeMainNav\(\)">首页 \(Home\)</a>
      <a onclick="togglePublicTab\('ladder'\); closeMainNav\(\)">天梯榜 \(Leaderboard\)</a>
      <a onclick="openArchiveView\(\); closeMainNav\(\)">赛事与活动中心 \(Events\)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4>专属入口 \(Portals\)</h4>
      <a onclick="togglePublicTab\('login'\); closeMainNav\(\)">学员专属登录 \(Student Login\)</a>
      <a href="school.html">校际赛报名系统 \(Schools\)</a>
      <a href="admin.html">教练管理端 \(Admin\)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4>系统语言 \(Language\)</h4>
      <a onclick="setLang\('cn'\); closeMainNav\(\)">中文 \(Chinese\)</a>
      <a onclick="setLang\('bm'\); closeMainNav\(\)">Bahasa Melayu \(BM\)</a>
      <a onclick="setLang\('en'\); closeMainNav\(\)">English \(EN\)</a>
    </div>'''

mega_new = '''<div class="apple-mega-col">
      <h4 data-i18n="nav.explore">探索俱乐部 (Explore)</h4>
      <a onclick="togglePublicTab('home'); closeMainNav()" data-i18n="nav.home">🏠 首页 (Home)</a>
      <a onclick="togglePublicTab('ladder'); closeMainNav()" data-i18n="nav.ladder">🏆 天梯榜 (Leaderboard)</a>
      <a onclick="openArchiveView(); closeMainNav()" data-i18n="events.title">📸 赛事与活动中心 (Events)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4 data-i18n="nav.portals">专属入口 (Portals)</h4>
      <a onclick="togglePublicTab('login'); closeMainNav()" data-i18n="nav.student_login">🔐 学员专属登录 (Student Login)</a>
      <a href="school.html" data-i18n="nav.school_portal">🏫 校际赛报名系统 (Schools)</a>
      <a href="admin.html" data-i18n="nav.admin_portal">👑 教练管理端 (Admin)</a>
    </div>
    
    <div class="apple-mega-col">
      <h4 data-i18n="nav.language">系统语言 (Language)</h4>
      <a onclick="setLang('cn'); closeMainNav()">🇨🇳 中文 (Chinese)</a>
      <a onclick="setLang('bm'); closeMainNav()">🇲🇾 Bahasa Melayu</a>
      <a onclick="setLang('en'); closeMainNav()">🇬🇧 English</a>
    </div>'''

text = re.sub(mega_old, mega_new, text)

# 2. Add translation keys to JS
nav_keys = '''    "nav.explore": "探索俱乐部 (Explore)",
    "nav.portals": "专属入口 (Portals)",
    "nav.student_login": "学员专属登录 (Student Login)",
    "nav.school_portal": "校际赛报名系统 (Schools)",
    "nav.admin_portal": "教练管理端 (Admin)",
    "nav.language": "系统语言 (Language)",'''

# Insert after "nav.menu"
text = text.replace('"nav.menu": "菜单",', '"nav.menu": "菜单",\n' + nav_keys)
text = text.replace('"nav.menu": "Menu",', '"nav.menu": "Menu",\n' + nav_keys.replace("探索俱乐部 (Explore)", "Terokai Kelab (Explore)").replace("专属入口 (Portals)", "Portal Khas (Portals)").replace("学员专属登录 (Student Login)", "Log Masuk Pelajar (Student)").replace("校际赛报名系统 (Schools)", "Sistem Antara Sekolah (Schools)").replace("教练管理端 (Admin)", "Portal Jurulatih (Admin)").replace("系统语言 (Language)", "Bahasa Sistem (Language)"))

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Mega Menu translation applied.")
