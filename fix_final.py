import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# --- 1. Fix Missing Translations in index.html ---
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Inject into CN
cn_inject = '''"events.sub": "记录百乐县中国象棋公会的精彩瞬间与赛事资源",
    "nav.explore": "探索俱乐部 (Explore)",
    "nav.portals": "专属入口 (Portals)",
    "nav.student_login": "学员专属登录 (Student Login)",
    "nav.school_portal": "校际赛报名系统 (Schools)",
    "nav.admin_portal": "教练管理端 (Admin)",
    "nav.language": "系统语言 (Language)",
    "nav.menu": "菜单",'''
text = re.sub(r'"events\.sub": "记录百乐县中国象棋公会的精彩瞬间与赛事资源",', cn_inject, text)

# Inject into BM
bm_inject = '''"events.sub": "Sumber dan Rekod Acara CXQB",
    "nav.explore": "Terokai Kelab (Explore)",
    "nav.portals": "Portal Khas (Portals)",
    "nav.student_login": "Log Masuk Pelajar (Student)",
    "nav.school_portal": "Sistem Antara Sekolah (Schools)",
    "nav.admin_portal": "Portal Jurulatih (Admin)",
    "nav.language": "Bahasa Sistem (Language)",
    "nav.menu": "Menu",'''
text = re.sub(r'"events\.sub": "Sumber dan Rekod Acara CXQB",', bm_inject, text)

# Inject into EN
en_inject = '''"events.sub": "CXQB Event Resources and Records",
    "nav.explore": "Explore Club",
    "nav.portals": "Portals",
    "nav.student_login": "Student Login",
    "nav.school_portal": "Schools Portal",
    "nav.admin_portal": "Admin Portal",
    "nav.language": "System Language",
    "nav.menu": "Menu",'''
text = re.sub(r'"events\.sub": "CXQB Event Resources and Records",', en_inject, text)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)


# --- 2. Upgrade Admin and School Login Cards ---
for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to change the .login-card CSS to dark theme
    old_login_card_css = r'\.login-card\{background:#FFF;border-radius:24px;padding:40px 32px;text-align:center;max-width:380px;width:100%;box-shadow:0 20px 60px rgba\(0,0,0,0\.3\);\}'
    new_login_card_css = '.login-card{background:rgba(6,23,36,0.9);border:1px solid rgba(255,255,255,0.1);border-radius:24px;padding:40px 32px;text-align:center;max-width:380px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5); backdrop-filter: blur(20px);}'
    content = re.sub(old_login_card_css, new_login_card_css, content)

    # Make the title and text light
    content = re.sub(r'\.login-card h1\{font-size:20px;font-weight:900;color:var\(--pri\);margin-bottom:6px;\}', '.login-card h1{font-size:20px;font-weight:900;color:#fff;margin-bottom:6px;}', content)
    content = re.sub(r'\.login-card \.sub\{font-size:13px;color:var\(--text2\);margin-bottom:24px;\}', '.login-card .sub{font-size:13px;color:rgba(255,255,255,0.6);margin-bottom:24px;}', content)

    # Upgrade the inputs to dark theme
    content = re.sub(r'\.pin-input\{.*?\}', '.pin-input{width:100%;padding:14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;font-size:15px;font-weight:700;text-align:center;color:#fff;outline:none;transition:0.3s;} .pin-input:focus{border-color:#F1C40F; background:rgba(255,255,255,0.1);}', content)

    # Change the login button color to navy/gold
    content = re.sub(r'\.login-btn\{.*?\}', '.login-btn{width:100%;padding:14px;background:#040C17;color:#fff;border:1px solid rgba(255,255,255,0.1);border-radius:12px;font-size:15px;font-weight:800;cursor:pointer;transition:all 0.3s; margin-top: 10px;} .login-btn:hover{background:#F1C40F;color:#000;border-color:#F1C40F;}', content)
    
    # Change body text colors
    content = content.replace('color:var(--pri3)', 'color:rgba(255,255,255,0.8)')
    content = content.replace('color:var(--text3)', 'color:rgba(255,255,255,0.5)')
    
    # The logo background is white in admin.html, remove it or make it transparent
    content = re.sub(r'\.login-logo\{width:80px;height:80px;border-radius:50%;margin-bottom:20px;box-shadow:0 8px 24px rgba\(0,0,0,0\.12\);\}', '.login-logo{width:80px;height:80px;border-radius:50%;margin-bottom:20px;box-shadow:0 8px 24px rgba(0,0,0,0.3); border: 2px solid rgba(241,196,15,0.4);}', content)
    
    # Fix segmented control colors for dark mode in admin.html/school.html
    # In my previous script, I gave it a white background for active span.
    old_lang_css = r'\.lang-switcher span\.active \{\s*background: #FFF;\s*color: #0F172A;\s*box-shadow: 0 2px 8px rgba\(0,0,0,0\.1\);\s*\}'
    new_lang_css = '.lang-switcher span.active { background: rgba(255,255,255,0.9); color: #000; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }'
    content = re.sub(old_lang_css, new_lang_css, content, flags=re.DOTALL)
    
    # Also change inactive text color
    content = content.replace('color: #64748B;', 'color: rgba(255,255,255,0.5);')

    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Translations fixed and Login cards themed!")
