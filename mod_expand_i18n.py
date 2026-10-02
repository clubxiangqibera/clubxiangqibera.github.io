import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Increase Logo Size
text = text.replace('height: 48px;', 'height: 90px;')

# 2. Add data-i18n to Badges (wrap the text in a span if needed, or replace the whole content)
text = text.replace('全县唯一象棋教育学院</span>', '<span data-i18n="hero.badge1">全县唯一象棋教育学院</span></span>')
text = text.replace('CXQB ELO 官方排位</span>', '<span data-i18n="hero.badge2">CXQB ELO 官方排位</span></span>')
text = text.replace('5 级段位考评体系</span>', '<span data-i18n="hero.badge3">5 级段位考评体系</span></span>')

# 3. Add data-i18n to Announce section
text = text.replace('✅ 报名开放中</span>', '✅ <span data-i18n="camp.status">报名开放中</span></span>')
text = text.replace('<h2 class="announce__title">2026 第一届「棋缘」中国象棋启蒙教育营</h2>', '<h2 class="announce__title" data-i18n="camp.title">2026 第一届「棋缘」中国象棋启蒙教育营</h2>')
text = text.replace('日期：11月22日 (星期日)</li>', '<span data-i18n="camp.date">日期：11月22日 (星期日)</span></li>')
text = text.replace('地点：Dewan SJK(C) Triang 1</li>', '<span data-i18n="camp.location">地点：Dewan SJK(C) Triang 1</span></li>')
text = text.replace('亮点：零基础教学 · 全套教材 · 结业证书</li>', '<span data-i18n="camp.highlight">亮点：零基础教学 · 全套教材 · 结业证书</span></li>')
text = text.replace('>立即填写 Google Form 报名表</a>', ' data-i18n="camp.btn">立即填写 Google Form 报名表</a>')

# 4. Add data-i18n to Gallery section
text = text.replace('<h2 class="section__title">历届活动相册</h2>', '<h2 class="section__title" data-i18n="gallery.title">历届活动相册</h2>')
text = text.replace('<p class="section__sub">记录在百乐县中国象棋公会的精彩瞬间</p>', '<p class="section__sub" data-i18n="gallery.sub">记录在百乐县中国象棋公会的精彩瞬间</p>')
text = text.replace('<div class="empty">暂无公开相册。</div>', '<div class="empty" data-i18n="gallery.empty">暂无公开相册。</div>')

# 5. Add data-i18n to Ladder section
text = text.replace('<h2 class="section__title">百乐全县青少年天梯三甲</h2>', '<h2 class="section__title" data-i18n="ladder.title">百乐全县青少年天梯三甲</h2>')
text = text.replace('<p class="section__sub">CXQB ELO 官方排位体系 · 实时同步</p>', '<p class="section__sub" data-i18n="ladder.sub">CXQB ELO 官方排位体系 · 实时同步</p>')

# 6. Replace the entire i18n script with the expanded one
new_script = '''
<script>
  // === CN/BM/EN Translation System ===
  const i18n = {
    cn: {
      "nav.home": "首页", "nav.ladder": "天梯榜", "nav.login": "登录",
      "hero.title": "百乐象棋俱乐部", "hero.tagline": "彭亨百乐 · 全县唯一中国象棋教育学院",
      "hero.badge1": "全县唯一象棋教育学院", "hero.badge2": "CXQB ELO 官方排位", "hero.badge3": "5 级段位考评体系",
      "camp.status": "报名开放中", "camp.title": "2026 第一届「棋缘」中国象棋启蒙教育营",
      "camp.date": "日期：11月22日 (星期日)", "camp.location": "地点：Dewan SJK(C) Triang 1", "camp.highlight": "亮点：零基础教学 · 全套教材 · 结业证书", "camp.btn": "立即填写 Google Form 报名表",
      "gallery.title": "历届活动相册", "gallery.sub": "记录在百乐县中国象棋公会的精彩瞬间", "gallery.empty": "暂无公开相册。",
      "ladder.title": "百乐全县青少年天梯三甲", "ladder.sub": "CXQB ELO 官方排位体系 · 实时同步",
      "footer.about_title": "百乐象棋俱乐部", "footer.about_desc": "Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。",
      "footer.partners_title": "认证机构 & 官方合作伙伴", "footer.contact_title": "联系方式"
    },
    bm: {
      "nav.home": "Utama", "nav.ladder": "Kedudukan", "nav.login": "Log Masuk",
      "hero.title": "Kelab XiangQi Bera", "hero.tagline": "Satu-satunya Akademi Catur Cina di Daerah Bera",
      "hero.badge1": "Akademi Catur Tunggal Bera", "hero.badge2": "Sistem ELO Rasmi CXQB", "hero.badge3": "Sistem Penilaian 5 Tahap",
      "camp.status": "Pendaftaran Dibuka", "camp.title": "Kem Asas Catur Cina «Qi Yuan» 2026",
      "camp.date": "Tarikh: 22 Nov (Ahad)", "camp.location": "Lokasi: Dewan SJK(C) Triang 1", "camp.highlight": "Fokus: Asas Sifar · Bahan Penuh · Sijil", "camp.btn": "Isi Borang Google Sekarang",
      "gallery.title": "Galeri Acara Lepas", "gallery.sub": "Merakam detik indah di Kelab Xiangqi Bera", "gallery.empty": "Tiada album awam setakat ini.",
      "ladder.title": "Top 3 Kedudukan Belia Bera", "ladder.sub": "Sistem ELO Rasmi CXQB · Segerak Langsung",
      "footer.about_title": "Kelab XiangQi Bera", "footer.about_desc": "Club XiangQi Bera (CXQB)<br>Institusi latihan dan pensijilan rasmi catur Cina di Bera.",
      "footer.partners_title": "Rakan Rasmi & Pensijilan", "footer.contact_title": "Hubungi Kami"
    },
    en: {
      "nav.home": "Home", "nav.ladder": "Ladder", "nav.login": "Login",
      "hero.title": "Club XiangQi Bera", "hero.tagline": "The Only Chinese Chess Academy in Bera District",
      "hero.badge1": "The Only Chess Academy in Bera", "hero.badge2": "CXQB Official ELO System", "hero.badge3": "5-Level Rating System",
      "camp.status": "Registration Open", "camp.title": "2026 1st «Qi Yuan» Xiangqi Beginner Camp",
      "camp.date": "Date: Nov 22 (Sun)", "camp.location": "Location: Dewan SJK(C) Triang 1", "camp.highlight": "Highlights: Zero Basics · Full Material · Certificate", "camp.btn": "Fill Google Form Now",
      "gallery.title": "Past Event Gallery", "gallery.sub": "Capturing wonderful moments at CXQB", "gallery.empty": "No public albums available.",
      "ladder.title": "Bera Youth Top 3 Ladder", "ladder.sub": "CXQB Official ELO System · Live Sync",
      "footer.about_title": "Club XiangQi Bera", "footer.about_desc": "Club XiangQi Bera (CXQB)<br>The official training and certification institution in Bera.",
      "footer.partners_title": "Official Partners", "footer.contact_title": "Contact Us"
    }
  };

  function setLang(lang, btnContext) {
    // Update active button state
    if(btnContext) {
      document.querySelectorAll('.lang button').forEach(b => b.setAttribute('aria-pressed', 'false'));
      btnContext.setAttribute('aria-pressed', 'true');
    }
    
    // Apply translations
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if(i18n[lang] && i18n[lang][key]) {
        el.innerHTML = i18n[lang][key];
      }
    });
  }
</script>
</body>
'''
text = re.sub(r'<script>\s*// === CN/BM/EN Translation System ===.*?</script>\s*</body>', new_script, text, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
