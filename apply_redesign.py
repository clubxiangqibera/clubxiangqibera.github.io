import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Original length:", len(text))

# 1. CLEAN CSS
# Remove legacy classes
legacy_patterns = [
    r'\.public-hero \{[^}]+\}',
    r'\.ph-logo \{[^}]+\}',
    r'\.ph-title \{[^}]+\}',
    r'\.ph-subtitle \{[^}]+\}',
    r'\.ph-tagline \{[^}]+\}',
    r'\.ph-stats-grid \{[^}]+\}',
    r'\.ph-stat-pill \{[^}]+\}',
    r'\.camp-banner \{[^}]+\}',
    r'\.camp-poster \{[^}]+\}',
    r'\.camp-badge \{[^}]+\}',
    r'\.camp-title \{[^}]+\}',
    r'\.camp-details \{[^}]+\}',
    r'\.btn-wa \{[^}]+\}',
    r'\.podium-card \{[^}]+\}',
    r'\.podium-card\.rank-1 \{[^}]+\}',
    r'\.podium-card\.rank-2 \{[^}]+\}',
    r'\.podium-card\.rank-3 \{[^}]+\}',
    r'\.podium-card-inner \{[^}]+\}',
    r'\.podium-card-rating \{[^}]+\}',
    r'\.rank-badge \{[^}]+\}',
    r'\.rank1-label \{[^}]+\}',
    r'@keyframes float \{[^}]+\}'
]

for pat in legacy_patterns:
    text = re.sub(pat, '', text, flags=re.DOTALL)

# Remove unused variables
text = re.sub(r'--hero-bg:[^;]+;', '', text)
text = re.sub(r'--hero-border:[^;]+;', '', text)
text = re.sub(r'--glass-blur:[^;]+;', '', text)

# Restyle gate-card
text = re.sub(r'\.gate-card \{[^}]+\}', '.gate-card { background: var(--navy-900); padding: 40px; border-radius: var(--radius); width: 100%; max-width: 400px; box-shadow: var(--shadow); border: 1px solid var(--line); }', text)
text = re.sub(r'\.gate-title \{[^}]+\}', '.gate-title { font-family: var(--font-serif); font-size: 24px; font-weight: 700; color: var(--ink); margin: 0 0 8px; }', text)
text = re.sub(r'\.gate-sub \{[^}]+\}', '.gate-sub { font-size: 14px; color: var(--ink-dim); margin: 0 0 24px; }', text)
text = re.sub(r'\.gate-badge \{[^}]+\}', '.gate-badge { display: inline-block; background: var(--gold); color: var(--navy-950); padding: 4px 12px; border-radius: var(--radius-pill); font-size: 12px; font-weight: 700; margin-bottom: 16px; }', text)
text = re.sub(r'\.gate-input \{[^}]+\}', '.gate-input { width: 100%; background: var(--navy-800); border: 1px solid var(--line); color: var(--ink); padding: 12px 16px; border-radius: var(--radius); font-size: 15px; margin-bottom: 16px; transition: border 0.2s; } .gate-input:focus { border-color: var(--gold); outline: none; }', text)
text = re.sub(r'\.login-btn \{[^}]+\}', '.login-btn { width: 100%; background: var(--red); color: #fff; border: none; padding: 14px; border-radius: var(--radius); font-size: 16px; font-weight: 700; cursor: pointer; transition: background 0.2s; } .login-btn:hover { background: var(--red-hover); }', text)

# Add rank-list styles
rank_list_css = '''
.rank-list { display: flex; flex-direction: column; gap: 12px; margin-top: 24px; }
.rank-list-item { display: flex; align-items: center; gap: 16px; padding: 16px 20px; background: var(--navy-900); border: 1px solid var(--line); border-radius: var(--radius); }
.rank-list-item__no { font: 700 1.1rem var(--font-serif); color: var(--gold-soft); width: 24px; text-align: center; }
.rank-list-item__info { flex: 1; }
.rank-list-item__name { font: 700 1.1rem var(--font-serif); color: var(--ink); }
.rank-list-item__school { font-size: 0.8rem; color: var(--ink-dim); margin-left: 8px; }
.rank-list-item__rating { font: 700 1.25rem var(--font-serif); color: var(--gold); }
'''
text = text.replace('</style>', rank_list_css + '\n</style>')

# 2. REWRITE HERO & CAMP HTML
# Replace public-hero block
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
else:
    print("Could not find hero block")

# Replace camp-banner block
old_camp = re.search(r'<!-- 2\. CAMP PROMO BANNER -->.*?<!-- 3\. MATCH TICKER -->', text, flags=re.DOTALL)
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

      <!-- 3. MATCH TICKER -->'''
    text = text.replace(old_camp.group(0), new_camp)
else:
    print("Could not find camp block")


# Update gallery
text = text.replace('<h2 class="section__title" data-i18n="gallery.title">历届活动相册</h2>', '<h2 class="section__title" data-i18n="gallery.title">历届活动相册</h2>')
text = text.replace('<p class="section__sub" data-i18n="gallery.sub">记录在百乐县中国象棋公会的精彩瞬间</p>', '<p class="section__sub" data-i18n="gallery.sub">记录在百乐县中国象棋公会的精彩瞬间</p>')
# Wrap gallery in section
gallery_start = text.find('<!-- 4. GALLERY -->')
gallery_end = text.find('<!-- 5. LADDER (REAL-TIME) -->')
if gallery_start != -1 and gallery_end != -1:
    old_gal = text[gallery_start:gallery_end]
    new_gal = '''<!-- 4. GALLERY -->
      <section class="section" id="gallery">
        <div class="section__head">
          <h2 class="section__title" data-i18n="gallery.title">历届活动相册</h2>
          <p class="section__sub" data-i18n="gallery.sub">记录在百乐县中国象棋公会的精彩瞬间</p>
        </div>
        <div id="publicGalleryArea">
          <div class="empty" data-i18n="gallery.empty">暂无公开相册。</div>
        </div>
      </section>

      '''
    text = text.replace(old_gal, new_gal)

# 3. FIX LADDER JS renderPublicLadder()
# We need to replace the entire renderPublicLadder function
old_render_js = re.search(r'function renderPublicLadder\(players\) \{.*?\n    \}\n  \}\n', text, flags=re.DOTALL)
if not old_render_js:
    # try a wider match
    old_render_js = re.search(r'function renderPublicLadder\(players\) \{.*?container\.innerHTML = html;\n\}', text, flags=re.DOTALL)

if old_render_js:
    new_render_js = '''function renderPublicLadder(players) {
  const container = document.getElementById('publicRankList');
  if(!players || players.length === 0) {
    container.innerHTML = '<div class="empty">暂无排位数据。</div>';
    return;
  }
  
  // Sort descending
  const sorted = [...players].sort((a,b) => (b.rating || 0) - (a.rating || 0));
  
  // Top 3
  let html = '<div class="podium">';
  for (let i = 0; i < 3 && i < sorted.length; i++) {
    const p = sorted[i];
    const rank = i + 1;
    // We order them visually: 2nd, 1st, 3rd
    const visualOrder = rank === 1 ? 2 : (rank === 2 ? 1 : 3);
    const cssClass = `rank-card rank-card--${rank}`;
    
    const cardHtml = `
      <div class="${cssClass}" style="order: ${visualOrder}">
        <div class="rank-card__no">${rank}</div>
        <div class="rank-card__name">${p.name}</div>
        <div class="rank-card__school">${p.school || 'CXQB'}</div>
        <span class="rank-card__title">${p.title || '无段位'}</span>
        <span class="rank-card__rating">${p.rating || 1000}</span>
      </div>
    `;
    html += cardHtml;
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
          <div class="rank-list-item__rating">${p.rating || 1000}</div>
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

# 4. FIX LOGIN GATE
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
    
# Fix placeholder attributes for i18n
# Add placeholder handling to setLang function
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

print("New length:", len(text))

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
