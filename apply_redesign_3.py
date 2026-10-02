import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace gate-card HTML
old_gate = re.search(r'<div class="gate-card".*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if old_gate:
    new_login_gate = '''<div class="gate-card" style="margin:20px auto;">
        <div class="gate-badge" data-i18n="login.badge">🏛️ CLUB XIANGQI BERA · 学员专属登录</div>
        <h1 class="gate-title" data-i18n="login.title">百乐象棋俱乐部</h1>
        <p class="gate-sub" data-i18n="login.sub">请使用俱乐部发放的学员账号密码登录</p>

        <div class="input-group">
          <label class="input-label" data-i18n="login.name_label">👤 学员姓名 (Name)</label>
          <input type="text" id="nameInput" class="gate-input input" placeholder="如: 黄梓轩 或 admin" data-i18n="login.name_ph" autofocus>
        </div>

        <div class="input-group">
          <label class="input-label" data-i18n="login.pwd_label">🔑 专属密码 (Password)</label>
          <input type="password" id="pwdInput" class="gate-input input" placeholder="请输入密码" data-i18n="login.pwd_ph">
        </div>

        <button class="login-btn btn btn--primary" onclick="handleLogin()" data-i18n="login.btn">🔐 登录进入系统</button>
        <div id="loginMsg" style="color:var(--red);font-size:13px;font-weight:800;margin-top:10px;display:none;"></div>

      </div>
    </div>
  </div>'''
    text = text.replace(old_gate.group(0), new_login_gate)
else:
    print("Could not find gate card")

# Replace renderPublicLadder function
old_render = re.search(r'function renderPublicLadder\(players\) \{.*?container\.innerHTML = html;\n\}', text, flags=re.DOTALL)
if not old_render:
    old_render = re.search(r'function renderPublicLadder\(players\) \{.*?\n  \}\n\}', text, flags=re.DOTALL)
    
if old_render:
    new_render_js = '''function renderPublicLadder(players) {
  const container = document.getElementById('publicPodiumArea');
  if(!players || players.length === 0) {
    container.innerHTML = '<div class="empty">暂无排位数据。</div>';
    return;
  }
  
  // Sort descending
  const sorted = [...players].sort((a,b) => (b.elo || 0) - (a.elo || 0));
  
  // Top 3
  let html = '<div class="podium">';
  for (let i = 0; i < 3 && i < sorted.length; i++) {
    const p = sorted[i];
    const rank = i + 1;
    // We order them visually: 2nd, 1st, 3rd
    const visualOrder = rank === 1 ? 2 : (rank === 2 ? 1 : 3);
    const cssClass = `rank-card rank-card--${rank}`;
    
    html += `
      <div class="${cssClass}" style="order: ${visualOrder}">
        <div class="rank-card__no">${rank}</div>
        <div class="rank-card__name">${p.name}</div>
        <div class="rank-card__school">${p.school || 'CXQB'}</div>
        <span class="rank-card__title">${p.title || '无段位'}</span>
        <span class="rank-card__rating">${p.elo || 1000}</span>
      </div>
    `;
  }
  html += '</div>';

  // 4th and below
  if (sorted.length > 3) {
    html += '<div class="rank-list">';
    for (let i = 3; i < sorted.length; i++) {
      const p = sorted[i];
      const wins = p.stats ? p.stats.w : 0;
      const total = p.stats ? (p.stats.w + p.stats.d + p.stats.l) : 0;
      const winRate = total > 0 ? Math.round((wins / total) * 100) + '%' : '0%';
      
      html += `
        <div class="rank-list-item">
          <div class="rank-list-item__no">${i + 1}</div>
          <div class="rank-list-item__info">
            <span class="rank-list-item__name">${p.name}</span>
            <span class="rank-list-item__school">${p.school || 'CXQB'} · ${total}场 · 胜率 ${winRate}</span>
          </div>
          <div class="rank-list-item__rating">${p.elo || 1000}</div>
        </div>
      `;
    }
    html += '</div>';
  }
  
  container.innerHTML = html;
}'''
    text = text.replace(old_render.group(0), new_render_js)
else:
    print("Could not find render function")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")
