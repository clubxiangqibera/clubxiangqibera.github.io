import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# --- 1. Fix the Language Strings in index.html ---
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix HTML defaults
text = text.replace('探索俱乐部 (Explore)', '探索俱乐部')
text = text.replace('专属入口 (Portals)', '专属入口')
text = text.replace('系统语言 (Language)', '系统语言')

text = text.replace('🏠 首页 (Home)', '🏠 首页')
text = text.replace('🏆 天梯榜 (Leaderboard)', '🏆 天梯榜')
text = text.replace('📸 赛事与活动中心 (Events)', '📸 赛事与活动中心')

text = text.replace('🔐 学员专属登录 (Student Login)', '🔐 学员专属登录')
text = text.replace('🏫 校际赛报名系统 (Schools)', '🏫 校际赛报名系统')
text = text.replace('👑 教练管理端 (Admin)', '👑 教练管理端')

# Fix CN JS Translations
cn_old = '''"nav.explore": "探索俱乐部 (Explore)",
    "nav.portals": "专属入口 (Portals)",
    "nav.student_login": "学员专属登录 (Student Login)",
    "nav.school_portal": "校际赛报名系统 (Schools)",
    "nav.admin_portal": "教练管理端 (Admin)",
    "nav.language": "系统语言 (Language)",'''
cn_new = '''"nav.explore": "探索俱乐部",
    "nav.portals": "专属入口",
    "nav.student_login": "学员专属登录",
    "nav.school_portal": "校际赛报名系统",
    "nav.admin_portal": "教练管理端",
    "nav.language": "系统语言",'''
text = text.replace(cn_old, cn_new)

# Fix BM JS Translations
bm_old = '''"nav.explore": "Terokai Kelab (Explore)",
    "nav.portals": "Portal Khas (Portals)",
    "nav.student_login": "Log Masuk Pelajar (Student)",
    "nav.school_portal": "Sistem Antara Sekolah (Schools)",
    "nav.admin_portal": "Portal Jurulatih (Admin)",
    "nav.language": "Bahasa Sistem (Language)",'''
bm_new = '''"nav.explore": "Terokai Kelab",
    "nav.portals": "Portal Khas",
    "nav.student_login": "Log Masuk Pelajar",
    "nav.school_portal": "Sistem Antara Sekolah",
    "nav.admin_portal": "Portal Jurulatih",
    "nav.language": "Bahasa Sistem",'''
text = text.replace(bm_old, bm_new)

# Fix EN JS Translations
en_old = '''"nav.explore": "Explore Club",
    "nav.portals": "Portals",
    "nav.student_login": "Student Login",
    "nav.school_portal": "Schools Portal",
    "nav.admin_portal": "Admin Portal",
    "nav.language": "System Language",'''
en_new = '''"nav.explore": "Explore Club",
    "nav.portals": "Portals",
    "nav.student_login": "Student Login",
    "nav.school_portal": "Schools Portal",
    "nav.admin_portal": "Admin Portal",
    "nav.language": "System Language",'''
text = text.replace(en_old, en_new)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# --- 2. Fix the Backgrounds in admin.html and school.html ---
bg_css = '''
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 70%);
}
'''

for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Replace the gradient background with solid dark #040C17
    content = re.sub(r'background:\s*linear-gradient\([^)]+\);', 'background: #040C17;', content)
    
    # 2. Inject the grid pseudo-element
    if 'body::before' not in content:
        content = content.replace('</style>', bg_css + '\n</style>')
    
    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Language texts simplified and grid backgrounds applied.")
