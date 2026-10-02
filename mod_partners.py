import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove from top
pattern = r'<!-- 合作与认证机构 \(Partners\) -->.*?</div>\s*</div>'
text = re.sub(pattern, '', text, flags=re.DOTALL)

# 2. Add to bottom (before footer)
partners_bottom_html = '''
    <!-- 合作与认证机构 (Partners) -->
    <section class="section" style="text-align:center; padding-bottom: 40px; border-bottom: 1px solid var(--line-soft);">
      <span style="font-size: 0.85rem; color: var(--ink-dim); letter-spacing: 0.1em; text-transform: uppercase;">认证机构 & 官方合作伙伴</span>
      <div style="display:flex; flex-direction:column; align-items:center; gap:16px; margin-top:24px; opacity:0.85;">
        <img src="cxb_round_emblem.png" alt="Persatuan Logo" style="height: 64px; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.5));">
        <span style="font-family: var(--font-serif); font-size:1.25rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:0.05em;">Persatuan Catur Cina Daerah Bera</span>
      </div>
    </section>

  </div>

  <footer class="footer">
'''
text = text.replace('  </div>\n\n  <footer class="footer">', partners_bottom_html)
# If it couldn't find with two newlines, try one
if partners_bottom_html not in text:
    text = text.replace('  </div>\n  <footer class="footer">', partners_bottom_html)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
