import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace the entire footer section
# Let's find where the footer starts
footer_start = text.find('<footer class="footer">')
if footer_start != -1:
    # Find the end of the footer
    footer_end = text.find('</footer>', footer_start) + 9
    
    # We also need to remove the <section class="section"> that contains the partners if it's still outside.
    # Wait, in the previous script I put the section inside the footer? 
    # Ah! In my previous script:
    # <section class="section"...>...</section>
    # <div class="footer__legal">...</div>
    # So it was inside the footer!
    
    new_footer = '''<footer class="footer">
    <div class="footer__grid" style="grid-template-columns: 1fr 1fr 1fr; align-items: start; gap: 20px;">
      <!-- Col 1: About -->
      <div>
        <h3 data-i18n="footer.about_title">百乐象棋俱乐部</h3>
        <p><span data-i18n="footer.about_desc">Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。</span></p>
      </div>
      
      <!-- Col 2: Partners -->
      <div style="text-align: center;">
        <h3 style="margin-bottom: 16px;" data-i18n="footer.partners_title">认证机构 & 官方合作伙伴</h3>
        <div style="display:flex; flex-direction:column; align-items:center; gap:8px; opacity:0.85;">
          <img src="persatuan_emblem.png" alt="Persatuan Logo" style="height: 48px; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.5));">
          <span style="font-family: var(--font-serif); font-size:0.95rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:0.05em; line-height:1.2;">Persatuan Catur Cina Daerah Bera</span>
        </div>
      </div>

      <!-- Col 3: Contact -->
      <div style="text-align: right;">
        <h3 data-i18n="footer.contact_title">联系方式</h3>
        <p>Email: clubxiangqibera@gmail.com</p>
      </div>
    </div>
    
    <div class="footer__legal" style="margin-top: 32px; border-top: 1px solid var(--line-soft); padding-top: 24px; text-align: center;">
      © 2026 Club XiangQi Bera. All rights reserved.
    </div>
  </footer>'''
    
    text = text[:footer_start] + new_footer + text[footer_end:]

# 2. Add translation system JS and update Nav buttons
# Update Nav Buttons
text = text.replace('<button aria-pressed="true">中文</button>', '<button aria-pressed="true" onclick="setLang(\'cn\', this)">中文</button>')
text = text.replace('<button aria-pressed="false">BM</button>', '<button aria-pressed="false" onclick="setLang(\'bm\', this)">BM</button>')
text = text.replace('<button aria-pressed="false">EN</button>', '<button aria-pressed="false" onclick="setLang(\'en\', this)">EN</button>')

# Add data-i18n tags to some elements to test the system
text = text.replace('<h1 class="hero__title">百乐象棋俱乐部</h1>', '<h1 class="hero__title" data-i18n="hero.title">百乐象棋俱乐部</h1>')
text = text.replace('<p class="hero__tagline">彭亨百乐 · 全县唯一中国象棋教育学院</p>', '<p class="hero__tagline" data-i18n="hero.tagline">彭亨百乐 · 全县唯一中国象棋教育学院</p>')
text = text.replace('<a href="#hero" aria-current="page">首页</a>', '<a href="#hero" aria-current="page" data-i18n="nav.home">首页</a>')
text = text.replace('<a href="#ladder">天梯榜</a>', '<a href="#ladder" data-i18n="nav.ladder">天梯榜</a>')
text = text.replace('登录\n      </a>', '<span data-i18n="nav.login">登录</span>\n      </a>')

# The script
i18n_script = '''
<script>
  // === CN/BM/EN Translation System ===
  const i18n = {
    cn: {
      "nav.home": "首页", "nav.ladder": "天梯榜", "nav.login": "登录",
      "hero.title": "百乐象棋俱乐部", "hero.tagline": "彭亨百乐 · 全县唯一中国象棋教育学院",
      "footer.about_title": "百乐象棋俱乐部", "footer.about_desc": "Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。",
      "footer.partners_title": "认证机构 & 官方合作伙伴", "footer.contact_title": "联系方式"
    },
    bm: {
      "nav.home": "Utama", "nav.ladder": "Kedudukan", "nav.login": "Log Masuk",
      "hero.title": "Kelab XiangQi Bera", "hero.tagline": "Satu-satunya Akademi Catur Cina di Daerah Bera",
      "footer.about_title": "Kelab XiangQi Bera", "footer.about_desc": "Club XiangQi Bera (CXQB)<br>Institusi latihan dan pensijilan rasmi catur Cina di Bera.",
      "footer.partners_title": "Rakan Rasmi & Pensijilan", "footer.contact_title": "Hubungi Kami"
    },
    en: {
      "nav.home": "Home", "nav.ladder": "Ladder", "nav.login": "Login",
      "hero.title": "Club XiangQi Bera", "hero.tagline": "The Only Chinese Chess Academy in Bera District",
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
        el.innerHTML = i18n[lang][key]; // innerHTML allows <br> to work
      }
    });
  }
</script>
</body>
'''
text = text.replace('</body>', i18n_script)

# Add media query for mobile responsiveness for the footer grid
css_mobile = '''
@media (max-width: 768px) {
  .footer__grid { grid-template-columns: 1fr !important; text-align: center !important; }
  .footer__grid > div { text-align: center !important; }
}
'''
text = text.replace('</style>', css_mobile + '</style>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
