import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# --- admin.html ---
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Logo and Title with Gold Pill and Title
old_header = r'<img src="cxb_round_emblem\.png".*?<p class="sub" id="aSub">.*?</p>'
new_header = '''
    <div style="display:inline-block; background:#F1C40F; color:#0A1929; padding:6px 12px; border-radius:30px; font-size:12px; font-weight:800; margin-bottom:20px;">👑 CLUB XIANGQI BERA · 教练管理端</div>
    <h1 id="aTitle" style="font-family: 'Noto Serif SC', serif; font-size: 26px; color: #fff; margin-bottom: 8px; font-weight:900;">百乐象棋俱乐部</h1>
    <p class="sub" id="aSub" style="font-size: 14px; color: rgba(255,255,255,0.6); margin-bottom: 32px;">请使用俱乐部发放的教练密码登入后台</p>
'''
text = re.sub(old_header, new_header, text, flags=re.DOTALL)

# Add Label above Input
old_input = r'<div class="login-input-wrap">\s*<input type="password" id="adminPinInput" class="pin-input" placeholder="输入管理密码 \(Enter Password\)" maxlength="16" autofocus autocomplete="current-password">\s*</div>'
new_input = '''<div class="login-input-wrap" style="text-align:left; margin-bottom: 32px;">
        <label id="aLbl" style="display:block; font-size:13px; font-weight:700; color:rgba(255,255,255,0.5); margin-bottom:8px;">🔑 管理密码 (Admin Password)</label>
        <input type="password" id="adminPinInput" class="pin-input" placeholder="请输入密码" maxlength="16" autofocus autocomplete="current-password" style="text-align:left;">
      </div>'''
text = re.sub(old_input, new_input, text)

# Change Button to Red
text = re.sub(r'class="login-btn" id="aBtn"[^>]*>.*?<\/button>', 'class="login-btn" id="aBtn" style="background:linear-gradient(135deg, #E63946 0%, #D90429 100%); color:#fff; border:none; box-shadow:0 4px 15px rgba(217,4,41,0.3);">🚨 登录进入系统</button>', text)

# Remove the red border of pin-input error and simplify
text = text.replace('.pin-input {', '.pin-input { text-align: left; ')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)


# --- school.html ---
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Logo and Title with Gold Pill and Title
old_school_header = r'<!-- Official Club Emblem Header -->.*?<!-- System Title -->'
new_school_header = '''
    <div style="display:inline-block; background:#F1C40F; color:#0A1929; padding:6px 12px; border-radius:30px; font-size:12px; font-weight:800; margin-bottom:20px;">🏫 CLUB XIANGQI BERA · 校际赛报名系统</div>
    <!-- System Title -->'''
text = re.sub(old_school_header, new_school_header, text, flags=re.DOTALL)

# Adjust title font
text = re.sub(r'<h1 id="sTitle" style="font-size: 22px; font-weight: 900;.*?<\/h1>', '<h1 id="sTitle" style="font-family: \'Noto Serif SC\', serif; font-size: 26px; font-weight: 900; color: #fff; margin-bottom: 8px; letter-spacing: 1px;">校内象棋比赛管理系统</h1>', text)
text = re.sub(r'<p class="sub" id="sSub"[^>]*>.*?<\/p>', '<p class="sub" id="sSub" style="font-size: 14px; color: rgba(255,255,255,0.6); margin-bottom: 32px; font-weight:500;">百乐象棋对阵编排系统 · 自动破同分 · 现场大屏投影</p>', text)

# Add Label above Input
old_school_input = r'<div class="login-input-wrap">\s*<input type="text" id="schoolPinInput" class="pin-input"[^>]*>\s*</div>'
new_school_input = '''<div class="login-input-wrap" style="text-align:left; margin-bottom: 32px;">
        <label id="sLbl" style="display:block; font-size:13px; font-weight:700; color:rgba(255,255,255,0.5); margin-bottom:8px;">🔑 比赛授权码 (Access Code)</label>
        <input type="text" id="schoolPinInput" class="pin-input" placeholder="输入授权码 (如 CXQB-8888)" maxlength="16" autofocus autocomplete="off" style="text-align:left;">
      </div>'''
text = re.sub(old_school_input, new_school_input, text)

# Change Button to Red
text = re.sub(r'<button type="button"[^>]*id="sBtn"[^>]*>.*?<\/button>', '<button type="button" class="login-btn" id="sBtn" onclick="doSchoolLogin()" style="width:100%; padding:14px; border-radius:12px; font-size:15px; font-weight:800; background:linear-gradient(135deg, #E63946 0%, #D90429 100%); color:#fff; border:none; box-shadow:0 4px 15px rgba(217,4,41,0.3); cursor:pointer; margin-top:10px; transition:all 0.3s;">🚨 验证授权并进入比赛台</button>', text)

with io.open('school.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Redesigned admin and school to match student login!")
