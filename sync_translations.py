import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# --- admin.html ---
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the whole if blocks
old_logic = r"if\(lang === 'zh'\) \{.*?\}(?=\s*</script>|\s*window\.addEventListener)"
new_logic = '''if(lang === 'zh') {
        document.getElementById('adminPinInput').placeholder = '请输入密码';
        document.getElementById('aBtn').textContent = '🚨 登录进入系统';
        document.getElementById('loginError').textContent = '❌ 密码错误，请重新输入 (Invalid Password)';
        document.getElementById('aReturn').textContent = '← 返回主页 (Return to Menu)';
        const t = document.getElementById('aTitle'); if(t) t.textContent = '百乐象棋俱乐部';
        const s = document.getElementById('aSub'); if(s) s.textContent = '请使用俱乐部发放的教练密码登入后台';
        const l = document.getElementById('aLbl'); if(l) l.textContent = '🔑 管理密码 (Admin Password)';
      }
      if(lang === 'bm') {
        document.getElementById('adminPinInput').placeholder = 'Sila masukkan kata laluan';
        document.getElementById('aBtn').textContent = '🚨 Log Masuk Sistem';
        document.getElementById('loginError').textContent = '❌ Kata Laluan Tidak Sah';
        document.getElementById('aReturn').textContent = '← Kembali ke Utama (Return)';
        const t = document.getElementById('aTitle'); if(t) t.textContent = 'Kelab XiangQi Bera';
        const s = document.getElementById('aSub'); if(s) s.textContent = 'Sila gunakan kata laluan jurulatih untuk log masuk';
        const l = document.getElementById('aLbl'); if(l) l.textContent = '🔑 Kata Laluan (Admin Password)';
      }
      if(lang === 'en') {
        document.getElementById('adminPinInput').placeholder = 'Please enter your password';
        document.getElementById('aBtn').textContent = '🚨 Login to System';
        document.getElementById('loginError').textContent = '❌ Invalid Password';
        document.getElementById('aReturn').textContent = '← Return to Menu';
        const t = document.getElementById('aTitle'); if(t) t.textContent = 'Club XiangQi Bera';
        const s = document.getElementById('aSub'); if(s) s.textContent = 'Please login with your admin password';
        const l = document.getElementById('aLbl'); if(l) l.textContent = '🔑 Admin Password';
      }
'''
text = re.sub(old_logic, new_logic, text, flags=re.DOTALL)
with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)


# --- school.html ---
with io.open('school.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic_school = r"if\(lang === 'zh'\) \{.*?\}(?=\s*</script>|\s*window\.addEventListener)"
new_logic_school = '''if(lang === 'zh') {
        document.getElementById('schoolPinInput').placeholder = '输入授权码 (如 CXQB-8888)';
        document.getElementById('sBtn').textContent = '🚨 验证授权并进入比赛台';
        document.getElementById('sError').textContent = '❌ 授权码无效 (Invalid Code)';
        document.getElementById('sReturn').textContent = '← 返回主页 (Return to Menu)';
        const t = document.getElementById('sTitle'); if(t) t.textContent = '校内象棋比赛管理系统';
        const s = document.getElementById('sSub'); if(s) s.textContent = '百乐象棋对阵编排系统 · 自动破同分 · 现场大屏投影';
        const l = document.getElementById('sLbl'); if(l) l.textContent = '🔑 比赛授权码 (Access Code)';
      }
      if(lang === 'bm') {
        document.getElementById('schoolPinInput').placeholder = 'Masukkan Kod (cth: CXQB-8888)';
        document.getElementById('sBtn').textContent = '🚨 Sahkan & Masuk Sistem';
        document.getElementById('sError').textContent = '❌ Kod Tidak Sah';
        document.getElementById('sReturn').textContent = '← Kembali ke Utama (Return)';
        const t = document.getElementById('sTitle'); if(t) t.textContent = 'Sistem Pertandingan Sekolah';
        const s = document.getElementById('sSub'); if(s) s.textContent = 'Sistem Pemadanan & Unjuran Skrin CXQB';
        const l = document.getElementById('sLbl'); if(l) l.textContent = '🔑 Kod Akses (Access Code)';
      }
      if(lang === 'en') {
        document.getElementById('schoolPinInput').placeholder = 'Enter Code (e.g. CXQB-8888)';
        document.getElementById('sBtn').textContent = '🚨 Verify & Enter System';
        document.getElementById('sError').textContent = '❌ Invalid Code';
        document.getElementById('sReturn').textContent = '← Return to Menu';
        const t = document.getElementById('sTitle'); if(t) t.textContent = 'School Tournament System';
        const s = document.getElementById('sSub'); if(s) s.textContent = 'CXQB Pairing & Screen Projection System';
        const l = document.getElementById('sLbl'); if(l) l.textContent = '🔑 Access Code';
      }
'''
text = re.sub(old_logic_school, new_logic_school, text, flags=re.DOTALL)
with io.open('school.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translation sync complete!")
