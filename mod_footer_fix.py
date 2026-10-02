import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

footer_html = '''
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
    
    <!-- 合作与认证机构 (Partners) -->
    <section class="section" style="text-align:center; padding-bottom: 40px; border-bottom: 1px solid var(--line-soft); margin-top:32px;">
      <span style="font-size: 0.85rem; color: var(--ink-dim); letter-spacing: 0.1em; text-transform: uppercase;">认证机构 & 官方合作伙伴</span>
      <div style="display:flex; flex-direction:column; align-items:center; gap:16px; margin-top:24px; opacity:0.85;">
        <img src="cxb_round_emblem.png" alt="Persatuan Logo" style="height: 64px; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));">
        <span style="font-family: var(--font-serif); font-size:1.25rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:0.05em;">Persatuan Catur Cina Daerah Bera</span>
      </div>
    </section>

    <div class="footer__legal">
      © 2026 Club XiangQi Bera. All rights reserved.
    </div>
  </footer>
</div> <!-- Close securityGate -->
'''

# Find the end of securityGate. It is the </div> right before <div id="authenticatedApp"
idx = text.find('<div id="authenticatedApp"')
if idx != -1:
    # find the </div> right before it
    before_auth = text[:idx]
    last_div_idx = before_auth.rfind('</div>')
    if last_div_idx != -1:
        text = text[:last_div_idx] + footer_html + '\n' + text[last_div_idx+6:]

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
