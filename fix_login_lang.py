import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Restore publicLoginSection
login_section = '''
  <!-- LOGIN SECTION -->
  <div id="publicLoginSection" style="display:none; justify-content:center; align-items:center; min-height:75vh;">
    <div class="gate-card" style="margin:20px auto; width: 100%; max-width: 440px; background: var(--navy-900); padding: 40px; border-radius: var(--radius); box-shadow: 0 20px 40px rgba(0,0,0,0.5); border: 1px solid var(--line);">
      <div class="gate-badge" data-i18n="login.badge" style="display:inline-block; background:var(--gold); color:var(--navy-950); padding:6px 12px; border-radius:30px; font-size:12px; font-weight:800; margin-bottom:20px;">🏛️ CLUB XIANGQI BERA · 学员专属登录</div>
      <h1 class="gate-title" data-i18n="login.title" style="font-family: var(--font-serif); font-size: 26px; color: var(--ink); margin-bottom: 8px;">百乐象棋俱乐部</h1>
      <p class="gate-sub" data-i18n="login.sub" style="font-size: 14px; color: var(--ink-dim); margin-bottom: 32px;">请使用俱乐部发放的学员账号密码登录</p>

      <div class="input-group" style="margin-bottom: 20px;">
        <label class="input-label" data-i18n="login.name_label" style="display:block; font-size:13px; font-weight:700; color:var(--ink-dim); margin-bottom:8px;">👤 学员姓名 (Name)</label>
        <input type="text" id="nameInput" class="gate-input input" placeholder="如: 黄梓轩 或 admin" data-i18n="login.name_ph" style="width:100%; padding:14px; background:var(--navy-800); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-size:15px; outline:none;" autofocus>
      </div>

      <div class="input-group" style="margin-bottom: 32px;">
        <label class="input-label" data-i18n="login.pwd_label" style="display:block; font-size:13px; font-weight:700; color:var(--ink-dim); margin-bottom:8px;">🔑 专属密码 (Password)</label>
        <input type="password" id="pwdInput" class="gate-input input" placeholder="请输入密码" data-i18n="login.pwd_ph" style="width:100%; padding:14px; background:var(--navy-800); border:1px solid var(--line); border-radius:8px; color:var(--ink); font-size:15px; outline:none;">
      </div>

      <button class="login-btn btn btn--primary" onclick="handleLogin()" data-i18n="login.btn" style="width:100%; padding:16px; background:var(--red); color:#fff; font-size:16px; font-weight:700; border:none; border-radius:8px; cursor:pointer;">🔐 登录进入系统</button>
      <div id="loginMsg" style="color:var(--red);font-size:13px;font-weight:800;margin-top:16px;display:none; text-align:center;"></div>
    </div>
  </div>
'''
# Insert right before footer
text = text.replace('<footer class="footer">', login_section + '\n  <footer class="footer">')

# 2. Advance the Language Switcher
css = '''
.lang-switcher {
  display: flex; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 4px; border: 1px solid var(--line);
}
.lang-btn {
  flex: 1; padding: 10px; border-radius: 8px; font-size: 13px; font-weight: 700; color: var(--ink-dim);
  background: transparent; border: 1px solid transparent; cursor: pointer; transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.lang-btn[aria-pressed="true"] {
  background: var(--navy-800); color: var(--gold); box-shadow: 0 4px 12px rgba(0,0,0,0.5); border-color: var(--gold);
}
.lang-btn:hover:not([aria-pressed="true"]) {
  color: var(--ink); background: rgba(255,255,255,0.05);
}
'''
text = text.replace('</style>', css + '\n</style>')

old_lang_html = r'<div class="lang" style="display: flex; gap: 8px;">.*?</div>'
new_lang_html = '''<div class="lang lang-switcher">
      <button onclick="setLang('cn', this); closeMainNav()" class="lang-btn" aria-pressed="true">中文</button>
      <button onclick="setLang('bm', this); closeMainNav()" class="lang-btn" aria-pressed="false">BM</button>
      <button onclick="setLang('en', this); closeMainNav()" class="lang-btn" aria-pressed="false">EN</button>
    </div>'''
text = re.sub(old_lang_html, new_lang_html, text, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Login fixed and Lang Switcher advanced.")
