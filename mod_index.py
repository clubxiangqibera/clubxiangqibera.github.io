import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1A
text = text.replace('<div class="gate-logo">♟️</div>', '<div class="gate-logo"><img src="cxb_round_emblem.png" alt="CXB" style="width:64px; height:64px; border-radius:50%; box-shadow:0 4px 16px rgba(0,0,0,0.2);"></div>')

# 1B
text = text.replace('<div class="sb-logo">♟️ CXQB 学生端</div>', '<div class="sb-logo"><img src="cxb_round_emblem.png" alt="CXB" style="width:28px; height:28px; border-radius:50%;"> CXQB 学生端</div>')
text = text.replace('♟️ 学员专区', '🎯 学员专区')

# 1C
text = text.replace("pwd === '8888'", "pwd === '7789'")

# 1D
text = text.replace('${typeof realIndex !== "undefined" ? realIndex + 1 : i + 1}', '${i + 1}')

# 1E
text = text.replace('color:var(--primary-dark); margin-top:4px;" id="hStatTotal"', 'color:#fff; margin-top:4px;" id="hStatTotal"')
text = text.replace('color:var(--primary-dark); margin-top:4px;" id="hStatWinRate"', 'color:#fff; margin-top:4px;" id="hStatWinRate"')
text = text.replace('color:var(--primary-dark); margin-top:4px;" id="hStatRecord"', 'color:#fff; margin-top:4px;" id="hStatRecord"')

# Task 2A
text = text.replace('<a onclick="switchView(\'viewMatchLog\', this)" class="sb-link">📜 实战棋谱</a>', '<a onclick="switchView(\'viewMatchLog\', this)" class="sb-link">📜 实战棋谱</a>\n      <a onclick="switchView(\'viewGallery\', this)" class="sb-link">📸 活动相册</a>')

# Task 5A
text = text.replace('<a onclick="switchView(\'viewGallery\', this)" class="sb-link">📸 活动相册</a>', '<a onclick="switchView(\'viewGallery\', this)" class="sb-link">📸 活动相册</a>\n      <a onclick="switchView(\'viewSettings\', this)" class="sb-link">⚙️ 个人设置</a>')

# Task 2B & 5B
views_insert = """
    <!-- VIEW: GALLERY -->
    <div id="viewGallery" class="app-view">
      <div class="section-head" style="margin-top:20px;">
        <div class="section-title">📸 历届活动相册</div>
        <div class="section-sub">记录在百乐县中国象棋公会的精彩瞬间</div>
      </div>
      <div id="studentGalleryArea" style="display:grid; gap:16px; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); margin-top:16px; margin-bottom:50px; width:100%;">
        <div style="color:var(--text2); font-size:13px; padding:10px;">正在加载相册...</div>
      </div>
    </div> <!-- END VIEW GALLERY -->

    <!-- VIEW: SETTINGS -->
    <div id="viewSettings" class="app-view">
      <div class="section-head" style="margin-top:20px;">
        <div class="section-title">⚙️ 个人设置</div>
        <div class="section-sub">管理你的账号密码</div>
      </div>
      <div class="class-list-card" style="width:100%; max-width:500px; margin-bottom:50px;">
        <div class="class-list-header">
          <span>🔑 修改登录密码</span>
        </div>
        <div style="padding:24px;">
          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:800; margin-bottom:6px; color:var(--text);">当前密码</label>
            <input type="password" id="settingOldPwd" class="gate-input" placeholder="请输入当前密码">
          </div>
          <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:800; margin-bottom:6px; color:var(--text);">新密码</label>
            <input type="password" id="settingNewPwd" class="gate-input" placeholder="请输入新密码 (至少4位)">
          </div>
          <div style="margin-bottom:20px;">
            <label style="display:block; font-size:13px; font-weight:800; margin-bottom:6px; color:var(--text);">确认新密码</label>
            <input type="password" id="settingConfirmPwd" class="gate-input" placeholder="再次输入新密码">
          </div>
          <button onclick="changePassword()" style="width:100%; padding:14px; background:linear-gradient(135deg,var(--primary),var(--primary-mid)); color:#fff; border:none; border-radius:14px; font-size:15px; font-weight:900; cursor:pointer; box-shadow:0 6px 20px rgba(14,47,68,0.3);">
            🔐 确认修改密码
          </button>
          <div id="changePwdMsg" style="margin-top:12px; font-size:13px; font-weight:800; display:none; padding:10px; border-radius:10px;"></div>
        </div>
      </div>
    </div> <!-- END VIEW SETTINGS -->
"""
text = text.replace('</div> <!-- END VIEW MATCH LOGS -->', '</div> <!-- END VIEW MATCH LOGS -->\n' + views_insert)

# Task 2C
text = text.replace('renderMatchLogList(globalMatches);', 'renderMatchLogList(globalMatches);\n  loadStudentGallery();')

# Task 2D & 5C
js_insert = """
async function loadStudentGallery() {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/events');
    const data = await res.json();
    const events = data.events || data || [];
    const container = document.getElementById('studentGalleryArea');
    if(!container) return;
    if(!events || events.length === 0) {
      container.innerHTML = '<div style="color:var(--text2); font-size:13px; grid-column:1/-1; text-align:center; padding:30px;">暂无活动相册。</div>';
      return;
    }
    window._studentEvents = events;
    let html = '';
    events.forEach((evt, idx) => {
      const coverId = evt.photos && evt.photos.length > 0 ? evt.photos[0] : '';
      const coverUrl = coverId ? 'https://drive.google.com/thumbnail?sz=w800&id=' + coverId : '';
      html += `<div style="background:var(--card); border-radius:16px; overflow:hidden; box-shadow:var(--shadow); cursor:pointer; border:1.5px solid var(--border); transition:transform 0.2s;" onclick="openStudentEventPhotos(${idx})" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
        <div style="height:180px; background:#ddd url('${coverUrl}') center/cover;"></div>
        <div style="padding:16px;">
          <div style="font-weight:900; font-size:16px; color:var(--text); margin-bottom:6px;">${evt.name}</div>
          <div style="font-size:12px; color:var(--text2); margin-bottom:8px;">📅 ${evt.date} · 📸 ${evt.photos ? evt.photos.length : 0} 张照片</div>
          <div style="font-size:13px; color:var(--text2); line-height:1.4;">${evt.desc || ''}</div>
        </div>
      </div>`;
    });
    container.innerHTML = html;
  } catch(e) {
    const c = document.getElementById('studentGalleryArea');
    if(c) c.innerHTML = '<div style="color:var(--text2); font-size:13px;">相册加载失败。</div>';
  }
}

function openStudentEventPhotos(idx) {
  const evt = window._studentEvents[idx];
  if(!evt || !evt.photos) return;
  const container = document.getElementById('photoModalContent');
  container.innerHTML = `<div style="color:#fff; font-size:20px; font-weight:900; margin-bottom:10px;">${evt.name}</div>`;
  evt.photos.forEach(id => {
    container.innerHTML += `<img src="https://drive.google.com/thumbnail?sz=w800&id=${id}" style="width:100%; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.5); margin-bottom:16px;" loading="lazy">`;
  });
  document.getElementById('photoModal').style.display = 'flex';
}

async function changePassword() {
  const oldPwd = document.getElementById('settingOldPwd').value.trim();
  const newPwd = document.getElementById('settingNewPwd').value.trim();
  const confirmPwd = document.getElementById('settingConfirmPwd').value.trim();
  const msg = document.getElementById('changePwdMsg');

  if (!oldPwd || !newPwd || !confirmPwd) {
    msg.style.display = 'block';
    msg.style.background = '#FDEDEC';
    msg.style.color = 'var(--red)';
    msg.textContent = '❌ 请填写所有字段！';
    return;
  }

  if (newPwd.length < 4) {
    msg.style.display = 'block';
    msg.style.background = '#FDEDEC';
    msg.style.color = 'var(--red)';
    msg.textContent = '❌ 新密码至少4位！';
    return;
  }

  if (newPwd !== confirmPwd) {
    msg.style.display = 'block';
    msg.style.background = '#FDEDEC';
    msg.style.color = 'var(--red)';
    msg.textContent = '❌ 两次输入的新密码不一致！';
    return;
  }

  // Verify old password
  if (!currentUser || !currentUser.data) return;
  const stu = currentUser.data;
  const lvMatch = (stu.level || '').match(/Lv\s*(\d)/);
  const lvNum = lvMatch ? lvMatch[1] : '1';
  const idMatch = (stu.id || '').match(/(\d+)$/);
  const idNum = idMatch ? idMatch[1] : '001';
  const defaultPwd = lvNum + idNum;
  const currentPwd = stu.password && stu.password !== defaultPwd ? stu.password : (stu.password || defaultPwd);

  if (oldPwd !== currentPwd) {
    msg.style.display = 'block';
    msg.style.background = '#FDEDEC';
    msg.style.color = 'var(--red)';
    msg.textContent = '❌ 当前密码错误！';
    return;
  }

  // Send to GAS backend
  msg.style.display = 'block';
  msg.style.background = '#EBF5FB';
  msg.style.color = 'var(--primary-mid)';
  msg.textContent = '⏳ 正在修改密码...';

  try {
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({
        action: 'changePassword',
        studentId: stu.id,
        oldPassword: oldPwd,
        newPassword: newPwd
      })
    });
    const data = await res.json();
    if (data.success) {
      msg.style.background = '#E8F8F5';
      msg.style.color = 'var(--green)';
      msg.textContent = '✅ 密码修改成功！下次登录请使用新密码。';
      // Update local session
      currentUser.data.password = newPwd;
      localStorage.setItem('cxb_auth_user', JSON.stringify(currentUser));
      // Clear inputs
      document.getElementById('settingOldPwd').value = '';
      document.getElementById('settingNewPwd').value = '';
      document.getElementById('settingConfirmPwd').value = '';
    } else {
      msg.style.background = '#FDEDEC';
      msg.style.color = 'var(--red)';
      msg.textContent = '❌ ' + (data.error || '修改失败');
    }
  } catch(e) {
    msg.style.background = '#FDEDEC';
    msg.style.color = 'var(--red)';
    msg.textContent = '❌ 网络错误，请稍后再试。';
  }
}
"""
text = text.replace('// --- Public Gallery JS ---', js_insert + '\n// --- Public Gallery JS ---')

# Task 3
icons_old = """          <div class="icon-grid">
            <div class="icon-item" onclick="switchView('viewSchedule')">
              <div class="icon-circle">📅</div>
              <span class="icon-label">课程日程</span>
            </div>
            <div class="icon-item" onclick="switchView('viewSchedule')">
              <div class="icon-circle">💳</div>
              <span class="icon-label">学费缴交</span>
            </div>
            <div class="icon-item" onclick="switchView('viewLadder')">
              <div class="icon-circle">🏆</div>
              <span class="icon-label">全县排位</span>
            </div>
            <div class="icon-item" onclick="switchView('viewMatchLog')">
              <div class="icon-circle">📜</div>
              <span class="icon-label">实战记录</span>
            </div>
          </div>"""

icons_new = """          <div class="icon-grid">
            <div class="icon-item" onclick="switchView('viewSchedule')">
              <div class="icon-circle">📅</div>
              <span class="icon-label">课程日程</span>
            </div>
            <div class="icon-item" onclick="switchView('viewSchedule'); scrollToTuition();">
              <div class="icon-circle">💳</div>
              <span class="icon-label">学费缴交</span>
            </div>
            <div class="icon-item" onclick="switchView('viewLadder')">
              <div class="icon-circle">🏆</div>
              <span class="icon-label">全县排位</span>
            </div>
            <div class="icon-item" onclick="switchView('viewMatchLog')">
              <div class="icon-circle">📜</div>
              <span class="icon-label">实战记录</span>
            </div>
            <div class="icon-item" onclick="switchView('viewGallery')">
              <div class="icon-circle">📸</div>
              <span class="icon-label">活动相册</span>
            </div>
            <div class="icon-item" onclick="switchView('viewSettings')">
              <div class="icon-circle">⚙️</div>
              <span class="icon-label">个人设置</span>
            </div>
            <div class="icon-item" onclick="window.open('https://forms.gle/KUQu7MkUYLnvYeSd6','_blank')">
              <div class="icon-circle">📋</div>
              <span class="icon-label">活动报名</span>
            </div>
            <div class="icon-item" onclick="window.open('https://chat.whatsapp.com/your-group-link','_blank')">
              <div class="icon-circle">💬</div>
              <span class="icon-label">WhatsApp</span>
            </div>
          </div>"""
text = text.replace(icons_old, icons_new)

# Task 4A
matches_html = """
      <!-- RECENT MY MATCHES -->
      <div id="recentMyMatches" class="class-list-card" style="width:100%; margin-bottom:24px;">
        <div class="class-list-header">
          <span>⚔️ 最近实战对局</span>
          <span style="font-size:12px; cursor:pointer; color:var(--primary-light);" onclick="switchView('viewMatchLog')">查看全部 →</span>
        </div>
        <div id="recentMatchesBody" style="padding:0;">
        </div>
      </div>
"""
text = text.replace('<div class="ticker-wrap" style="margin-bottom:24px;width:100%;">', matches_html + '\n      <div class="ticker-wrap" style="margin-bottom:24px;width:100%;">')

# Task 4B
matches_js = """
  // Recent My Matches (last 5)
  const myMatches = globalMatches.filter(m => m.red === stu.cnName || m.black === stu.cnName);
  const recentBody = document.getElementById('recentMatchesBody');
  if (recentBody) {
    if (myMatches.length === 0) {
      recentBody.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text2); font-size:13px;">暂无对局记录</div>';
    } else {
      recentBody.innerHTML = myMatches.slice(-5).reverse().map(m => {
        const isRed = m.red === stu.cnName;
        const opponent = isRed ? m.black : m.red;
        const myColor = isRed ? '🔴 执红' : '⚫ 执黑';
        let resultText = '';
        let resultColor = '';
        if (m.result.includes('红胜')) {
          resultText = isRed ? '胜 ✅' : '负 ❌';
          resultColor = isRed ? 'var(--green)' : 'var(--red)';
        } else if (m.result.includes('黑胜')) {
          resultText = isRed ? '负 ❌' : '胜 ✅';
          resultColor = isRed ? 'var(--red)' : 'var(--green)';
        } else {
          resultText = '和 ➖';
          resultColor = 'var(--gold)';
        }
        return `<div style="display:flex; align-items:center; justify-content:space-between; padding:14px 20px; border-bottom:1px solid var(--border);">
          <div>
            <div style="font-weight:900; font-size:14px;">vs ${opponent}</div>
            <div style="font-size:12px; color:var(--text2); margin-top:2px;">${m.date} · ${m.round} · ${myColor}</div>
          </div>
          <div style="font-weight:900; font-size:14px; color:${resultColor};">${resultText}</div>
        </div>`;
      }).join('');
    }
  }
"""
text = text.replace('document.getElementById(\'hStatRecord\').textContent = `${lad.w || 0}胜 ${lad.d || 0}和 ${lad.l || 0}负`;\n}', 'document.getElementById(\'hStatRecord\').textContent = `${lad.w || 0}胜 ${lad.d || 0}和 ${lad.l || 0}负`;\n' + matches_js + '}')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("index.html updated successfully")
