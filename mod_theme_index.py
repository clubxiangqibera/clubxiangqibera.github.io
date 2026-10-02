import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with io.open('cxb-theme.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update CSS
# Append to the end of the <style> block, but before </style>
# This way, our new styles take precedence.
html = html.replace('</style>', css + '\n\n/* Custom rank list styles for 4th and below */\n.rank-list { display: flex; flex-direction: column; gap: 12px; margin-top: 24px; }\n.rank-list-item { display: flex; align-items: center; gap: 16px; padding: 16px 20px; background: var(--navy-900); border: 1px solid var(--line); border-radius: var(--radius); }\n.rank-list-item__no { font-family: var(--font-serif); font-size: 1.1rem; font-weight: 700; color: var(--gold-soft); width: 24px; text-align: center; }\n.rank-list-item__info { flex: 1; }\n.rank-list-item__name { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ink); }\n.rank-list-item__school { font-size: 0.8rem; color: var(--ink-dim); margin-left: 8px; }\n.rank-list-item__rating { font-family: var(--font-serif); font-size: 1.25rem; font-weight: 700; color: var(--gold); }\n\n</style>')

# 2. Re-write renderPublicLadder JS
old_js = r"html \+= `<div class=\"pod\">"
# Actually, let's just find the renderPublicLadder function and replace its body.
# We will use regex to find the function.
def replace_ladder_js(m):
    return """function renderPublicLadder(players) {
      const podium = document.getElementById('publicPodiumArea');
      const list = document.getElementById('publicRankList');
      if(!podium || !list) return;

      if(players.length === 0) {
        podium.innerHTML = '<div style="color:var(--text2); text-align:center; padding:20px;">暂无数据</div>';
        list.innerHTML = '';
        return;
      }

      // Render top 3 in the podium
      let podiumHtml = '';
      const top3 = players.slice(0, 3);
      
      const medals = [
        { rank: 1, class: 'rank-card--1', no: '1' },
        { rank: 2, class: 'rank-card--2', no: '2' },
        { rank: 3, class: 'rank-card--3', no: '3' }
      ];

      // Reorder top 3 for visual (2nd, 1st, 3rd)
      const visualOrder = [];
      if(top3.length > 1) visualOrder.push(top3[1]);
      if(top3.length > 0) visualOrder.push(top3[0]);
      if(top3.length > 2) visualOrder.push(top3[2]);

      visualOrder.forEach(p => {
        const medal = medals.find(m => m.rank === p.rank);
        if(!medal) return;
        podiumHtml += `
          <div class="rank-card ${medal.class}">
            <div class="rank-card__no">${medal.no}</div>
            <div class="rank-card__name">${p.Name}</div>
            <div class="rank-card__school">${p.School || ''}</div>
            <span class="rank-card__title">五级棋手</span>
            <span class="rank-card__rating">${p.ELO}</span>
            <div style="font-size:0.75rem; color:var(--ink-dim); margin-top:4px;">${p.TotalMatches}场实战 (${p.Wins}胜${p.Draws}和${p.Losses}负)</div>
          </div>
        `;
      });
      podium.innerHTML = podiumHtml;

      // Render the rest in the list
      let listHtml = '<div class="rank-list">';
      for(let i=3; i<players.length; i++) {
        const p = players[i];
        let winRate = "0%";
        if(p.TotalMatches > 0) winRate = Math.round((p.Wins / p.TotalMatches)*100) + "%";
        
        listHtml += `
          <div class="rank-list-item">
            <div class="rank-list-item__no">${p.rank}</div>
            <div class="rank-list-item__info">
              <span class="rank-list-item__name">${p.Name}</span>
              <span class="rank-list-item__school">${p.School || ''} · ${p.TotalMatches}场实战 (胜率 ${winRate})</span>
            </div>
            <div class="rank-list-item__rating">${p.ELO}</div>
          </div>
        `;
      }
      listHtml += '</div>';
      list.innerHTML = listHtml;
    }"""

html = re.sub(r'function renderPublicLadder\s*\([^)]*\)\s*\{.*?(?=\n    async function loadMatches)', replace_ladder_js, html, flags=re.DOTALL)

# 3. Replace the Security Gate HTML
# The easiest way is to read the old HTML, find <div id="securityGate"> and its end, and replace it.
# We will just replace everything between <div id="securityGate"> and <!-- === 登录弹窗 (Login Modal) === -->
new_public_html = """<div id="securityGate">
  <nav class="nav">
    <div class="nav__brand">
      <img src="cxb_round_emblem.png" alt="CXB Emblem" class="nav__logo">
      <div>
        <div class="nav__title">百乐象棋俱乐部</div>
        <span class="nav__sub">CLUB XIANGQI BERA</span>
      </div>
    </div>
    <div class="nav__links">
      <a href="#hero" aria-current="page">首页</a>
      <a href="#ladder">天梯榜</a>
      <a href="#" onclick="togglePublicTab('login')">
        <svg viewBox="0 0 24 24"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
        登录
      </a>
    </div>
  </nav>

  <div class="container">
    <header class="hero" id="hero">
      <img src="cxb_round_emblem.png" alt="CXB Logo" class="hero__logo">
      <h1 class="hero__title">百乐象棋俱乐部</h1>
      <div class="hero__en">CLUB XIANGQI BERA</div>
      <p class="hero__tagline">彭亨百乐 · 全县唯一中国象棋教育学院</p>
      <div class="hero__badges">
        <span class="badge"><svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg> 5+ 在册学员</span>
        <span class="badge"><svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> 3+ 实战对局</span>
        <span class="badge"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg> 5 级段位体系</span>
      </div>
    </header>

    <section class="section announce">
      <img src="poster_qiyuan_final.jpg" alt="2026 第一届「棋缘」教育营" class="announce__poster">
      <div>
        <span class="tag">🔥 火热招生中</span>
        <h2 class="announce__title">2026 第一届「棋缘」中国象棋启蒙教育营</h2>
        <ul class="meta">
          <li><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> 日期：11月22日 (星期日)</li>
          <li><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> 地点：Dewan SJK(C) Triang 1</li>
          <li><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polygon points="12 8 8 12 12 16 16 12 12 8"></polygon></svg> 亮点：零基础教学 · 全套教材 · 结业证书</li>
        </ul>
        <a href="https://forms.gle" target="_blank" class="btn btn--primary">立即填写 Google Form 报名表</a>
      </div>
    </section>

    <div class="ticker section">
      <div class="ticker__track" id="publicTickerTrack">
        <!-- JS fills this -->
      </div>
    </div>

    <section class="section" id="gallery">
      <div class="section__head">
        <h2 class="section__title">历届活动相册</h2>
        <p class="section__sub">记录在百乐县中国象棋公会的精彩瞬间</p>
      </div>
      <div id="publicGalleryArea">
        <div class="empty">暂无公开相册。</div>
      </div>
    </section>

    <section class="section" id="ladder">
      <div class="section__head">
        <h2 class="section__title">百乐全县青少年天梯三甲</h2>
        <p class="section__sub">CXQB ELO 官方排位体系 · 实时同步</p>
      </div>
      <div class="podium" id="publicPodiumArea"></div>
      <div id="publicRankList"></div>
    </section>
  </div>

  <footer class="footer">
    <div class="footer__grid" style="grid-template-columns: 2fr 1fr;">
      <div>
        <h3>百乐象棋俱乐部</h3>
        <p>Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。</p>
      </div>
      <div>
        <h3>联系方式</h3>
        <p>Email: clubxiangqibera@gmail.com</p>
      </div>
    </div>
    <div class="footer__legal">
      © 2026 Club XiangQi Bera. All rights reserved.
    </div>
  </footer>
</div>

"""

html = re.sub(r'<div id="securityGate">.*?<!-- === 登录弹窗 \(Login Modal\) === -->', new_public_html + '\n<!-- === 登录弹窗 (Login Modal) === -->', html, flags=re.DOTALL)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
