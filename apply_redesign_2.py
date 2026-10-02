import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace hero
old_hero = re.search(r'<!-- 1\. HERO SECTION -->.*?<!-- 2\. CAMP PROMO BANNER -->', text, flags=re.DOTALL)
if old_hero:
    new_hero = '''<!-- 1. HERO SECTION -->
      <header class="hero">
        <img src="cxb_round_emblem.png" alt="CXB Logo" class="hero__logo">
        <h1 class="hero__title" data-i18n="hero.title">百乐象棋俱乐部</h1>
        <div class="hero__en">CLUB XIANGQI BERA</div>
        <p class="hero__tagline" data-i18n="hero.tagline">彭亨百乐 · 全县唯一中国象棋教育学院</p>
        <div class="hero__badges">
          <span class="badge" data-i18n="hero.badge1">👑 全县唯一象棋教育学院</span>
          <span class="badge" data-i18n="hero.badge2">⚔️ CXQB ELO 官方排位</span>
          <span class="badge" data-i18n="hero.badge3">🏅 5 级段位考评体系</span>
        </div>
      </header>

      <!-- 2. CAMP PROMO BANNER -->'''
    text = text.replace(old_hero.group(0), new_hero)

# Replace camp banner
old_camp = re.search(r'<!-- 2\. CAMP PROMO BANNER -->.*?<!-- 3\. LIVE MATCH TICKER -->', text, flags=re.DOTALL)
if old_camp:
    new_camp = '''<!-- 2. CAMP PROMO BANNER -->
      <section class="announce section">
        <img src="poster_qiyuan_final.jpg" alt="棋缘教育营海报" class="announce__poster" onclick="openLightbox('poster_qiyuan_final.jpg')" style="cursor:pointer;">
        <div>
          <span class="tag" data-i18n="camp.status">✅ 报名开放中</span>
          <h2 class="announce__title" data-i18n="camp.title">2026 第一届「棋缘」中国象棋启蒙教育营</h2>
          <ul class="meta">
            <li><span data-i18n="camp.date">📅 日期：11月22日 (星期日)</span></li>
            <li><span data-i18n="camp.location">📍 地点：Dewan SJK(C) Triang 1</span></li>
            <li><span data-i18n="camp.highlight">🎯 亮点：零基础教学 · 全套教材 · 结业证书</span></li>
          </ul>
          <a href="https://forms.gle/KUQu7MkUYLnvYeSd6" target="_blank" class="btn btn--primary" data-i18n="camp.btn">📝 立即填写 Google Form 报名表</a>
        </div>
      </section>

      <!-- 3. LIVE MATCH TICKER -->'''
    text = text.replace(old_camp.group(0), new_camp)

# Replace match ticker structure
old_ticker = re.search(r'<!-- 3\. LIVE MATCH TICKER -->.*?<!-- 5\. EVENTS GALLERY -->', text, flags=re.DOTALL)
if old_ticker:
    new_ticker = '''<!-- 3. LIVE MATCH TICKER -->
      <section class="ticker section">
        <div id="publicTickerTrack" class="ticker__track"></div>
      </section>

      <!-- 4. EVENTS GALLERY -->'''
    text = text.replace(old_ticker.group(0), new_ticker)
else:
    # Just in case gallery is missing
    print("Could not find ticker to gallery")

# Gallery
old_gal = re.search(r'<div class="section-head".*?暂无公开相册。</div>\s*</div>', text, flags=re.DOTALL)
if old_gal:
    new_gal = '''<section class="section" id="gallery">
        <div class="section__head">
          <h2 class="section__title" data-i18n="gallery.title">历届活动相册</h2>
          <p class="section__sub" data-i18n="gallery.sub">记录在百乐县中国象棋公会的精彩瞬间</p>
        </div>
        <div id="publicGalleryArea">
          <div class="empty" data-i18n="gallery.empty">暂无公开相册。</div>
        </div>
      </section>'''
    text = text.replace(old_gal.group(0), new_gal)

# Ladder section HTML
old_ladder = re.search(r'<div class="section-head".*?publicPodiumArea"></div>\s*</div>', text, flags=re.DOTALL)
if old_ladder:
    new_ladder = '''<section class="section" id="ladder">
        <div class="section__head">
          <h2 class="section__title" data-i18n="ladder.title">百乐全县青少年天梯三甲</h2>
          <p class="section__sub" data-i18n="ladder.sub">CXQB ELO 官方排位体系 · 实时同步</p>
        </div>
        <div id="publicPodiumArea"></div>
      </section>'''
    text = text.replace(old_ladder.group(0), new_ladder)


# renderPublicLadder function
old_render_js = re.search(r'function renderPublicLadder\(players\).*?container\.innerHTML = html;\n\}', text, flags=re.DOTALL)
if not old_render_js:
    # fallback
    old_render_js = re.search(r'function renderPublicLadder\(players\) \{.*?\n    \}\n  \}\n', text, flags=re.DOTALL)

if old_render_js:
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
    text = text.replace(old_render_js.group(0), new_render_js)
else:
    print("Could not find renderPublicLadder function")

# Ticker JS
text = text.replace("item.className = 'ticker-item';", "item.className = 'ticker__item';")
text = text.replace("item.innerHTML = `<strong>${m.p1}</strong> <span style=\"color:#F1C40F\">${res}</span> <strong>${m.p2}</strong> <span style=\"font-size:11px;opacity:0.7;margin-left:8px;\">${m.date}</span>`;", "item.innerHTML = `<b>${m.p1}</b> <span class=\"ticker__score\">${res}</span> <b>${m.p2}</b> <span style=\"font-size:11px;opacity:0.7;margin-left:8px;\">${m.date}</span>`;")

# Login Gate HTML
login_gate = re.search(r'<div class="gate-card">.*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if login_gate:
    new_login_gate = '''<div class="gate-card">
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
    text = text.replace(login_gate.group(0), new_login_gate)
else:
    print("Could not find login gate block")
    
# Translation JS
js_i18n_search = re.search(r'const i18n = \{.*?\n  \};\n\n  function setLang\(lang, btnContext\) \{.*?\n  \}', text, flags=re.DOTALL)
if js_i18n_search:
    new_i18n_js = '''const i18n = {
  cn: {
    "nav.home": "首页", "nav.ladder": "天梯榜", "nav.login": "登录",
    "hero.title": "百乐象棋俱乐部",
    "hero.tagline": "彭亨百乐 · 全县唯一中国象棋教育学院",
    "hero.badge1": "👑 全县唯一象棋教育学院",
    "hero.badge2": "⚔️ CXQB ELO 官方排位",
    "hero.badge3": "🏅 5 级段位考评体系",
    "camp.status": "✅ 报名开放中",
    "camp.title": "2026 第一届「棋缘」中国象棋启蒙教育营",
    "camp.date": "📅 日期：11月22日 (星期日)",
    "camp.location": "📍 地点：Dewan SJK(C) Triang 1",
    "camp.highlight": "🎯 亮点：零基础教学 · 全套教材 · 结业证书",
    "camp.btn": "📝 立即填写 Google Form 报名表",
    "gallery.title": "历届活动相册",
    "gallery.sub": "记录在百乐县中国象棋公会的精彩瞬间",
    "gallery.empty": "暂无公开相册。",
    "ladder.title": "百乐全县青少年天梯排位",
    "ladder.sub": "CXQB ELO 官方排位体系 · 实时同步",
    "login.badge": "🏛️ CLUB XIANGQI BERA · 学员专属登录",
    "login.title": "百乐象棋俱乐部",
    "login.sub": "请使用俱乐部发放的学员账号密码登录",
    "login.name_label": "👤 学员姓名 (Name)",
    "login.name_ph": "如: 黄梓轩 或 admin",
    "login.pwd_label": "🔑 专属密码 (Password)",
    "login.pwd_ph": "请输入密码",
    "login.btn": "🔐 登录进入系统",
    "footer.about_title": "百乐象棋俱乐部",
    "footer.about_desc": "Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。",
    "footer.partners_title": "认证机构 & 官方合作伙伴",
    "footer.contact_title": "联系方式"
  },
  bm: {
    "nav.home": "Utama", "nav.ladder": "Kedudukan", "nav.login": "Log Masuk",
    "hero.title": "Kelab XiangQi Bera",
    "hero.tagline": "Satu-satunya Akademi Catur Cina di Daerah Bera, Pahang",
    "hero.badge1": "👑 Satu-satunya Akademi Catur di Bera",
    "hero.badge2": "⚔️ Sistem ELO Rasmi CXQB",
    "hero.badge3": "🏅 Penilaian 5 Tahap",
    "camp.status": "✅ Pendaftaran Dibuka",
    "camp.title": "Kem Asas Catur Cina «Qi Yuan» 2026",
    "camp.date": "📅 Tarikh: 22 Nov (Ahad)",
    "camp.location": "📍 Lokasi: Dewan SJK(C) Triang 1",
    "camp.highlight": "🎯 Asas Sifar · Bahan Penuh · Sijil Penyertaan",
    "camp.btn": "📝 Isi Borang Google Sekarang",
    "gallery.title": "Galeri Acara Lepas",
    "gallery.sub": "Merakam detik-detik indah bersama CXQB",
    "gallery.empty": "Tiada album awam setakat ini.",
    "ladder.title": "Top Kedudukan Belia Daerah Bera",
    "ladder.sub": "Sistem ELO Rasmi CXQB · Segerak Langsung",
    "login.badge": "🏛️ CLUB XIANGQI BERA · Log Masuk Pelajar",
    "login.title": "Kelab XiangQi Bera",
    "login.sub": "Sila gunakan akaun pelajar yang diberikan",
    "login.name_label": "👤 Nama Pelajar",
    "login.name_ph": "Contoh: Ahmad",
    "login.pwd_label": "🔑 Kata Laluan",
    "login.pwd_ph": "Masukkan kata laluan",
    "login.btn": "🔐 Log Masuk",
    "footer.about_title": "Kelab XiangQi Bera",
    "footer.about_desc": "Club XiangQi Bera (CXQB)<br>Institusi latihan dan pensijilan rasmi catur Cina di Bera, Pahang.",
    "footer.partners_title": "Rakan Rasmi & Pensijilan",
    "footer.contact_title": "Hubungi Kami"
  },
  en: {
    "nav.home": "Home", "nav.ladder": "Ladder", "nav.login": "Login",
    "hero.title": "Club XiangQi Bera",
    "hero.tagline": "The Only Chinese Chess Academy in Bera District, Pahang",
    "hero.badge1": "👑 The Only Chess Academy in Bera",
    "hero.badge2": "⚔️ CXQB Official ELO System",
    "hero.badge3": "🏅 5-Level Rating System",
    "camp.status": "✅ Registration Open",
    "camp.title": "2026 «Qi Yuan» Xiangqi Beginner Camp",
    "camp.date": "📅 Date: Nov 22 (Sunday)",
    "camp.location": "📍 Venue: Dewan SJK(C) Triang 1",
    "camp.highlight": "🎯 Zero Basics · Full Material · Certificate",
    "camp.btn": "📝 Fill Google Form Now",
    "gallery.title": "Past Event Gallery",
    "gallery.sub": "Capturing wonderful moments at CXQB",
    "gallery.empty": "No public albums available.",
    "ladder.title": "Bera Youth Ladder Rankings",
    "ladder.sub": "CXQB Official ELO System · Live Sync",
    "login.badge": "🏛️ CLUB XIANGQI BERA · Student Login",
    "login.title": "Club XiangQi Bera",
    "login.sub": "Please use the student credentials provided by the club",
    "login.name_label": "👤 Student Name",
    "login.name_ph": "e.g. Ahmad",
    "login.pwd_label": "🔑 Password",
    "login.pwd_ph": "Enter password",
    "login.btn": "🔐 Login",
    "footer.about_title": "Club XiangQi Bera",
    "footer.about_desc": "Club XiangQi Bera (CXQB)<br>The official training and certification institution in Bera, Pahang.",
    "footer.partners_title": "Official Partners",
    "footer.contact_title": "Contact Us"
  }
};

  function setLang(lang, btnContext) {
    if(btnContext) {
      document.querySelectorAll('.lang button').forEach(b => b.setAttribute('aria-pressed', 'false'));
      btnContext.setAttribute('aria-pressed', 'true');
    }
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if(i18n[lang] && i18n[lang][key]) {
        if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = i18n[lang][key];
        } else {
          el.innerHTML = i18n[lang][key];
        }
      }
    });
  }'''
    text = text.replace(js_i18n_search.group(0), new_i18n_js)
else:
    print("Could not find JS i18n block")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Applied successfully.")
