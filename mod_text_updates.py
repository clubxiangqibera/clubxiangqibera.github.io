import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Hero Badges
text = text.replace('5+ 在册学员', '全县唯一象棋教育学院')
text = text.replace('3+ 实战对局', 'CXQB ELO 官方排位')
text = text.replace('5 级段位体系', '5 级段位考评体系')

# 2. 火热招生中 -> 报名开放中
text = text.replace('🔥 火热招生中', '✅ 报名开放中')

# 3. Language Switcher in Nav Bar
nav_links_end = text.find('登录\n      </a>\n    </div>')
if nav_links_end != -1:
    lang_html = '''登录
      </a>
      <div class="lang">
        <button aria-pressed="true">中文</button>
        <button aria-pressed="false">BM</button>
        <button aria-pressed="false">EN</button>
      </div>
    </div>'''
    text = text.replace('登录\n      </a>\n    </div>', lang_html)

# 4. 合作单位标志 (Partner Logos)
partners_html = '''
    </header>

    <!-- 合作与认证机构 (Partners) -->
    <div style="text-align:center; margin-top: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--line-soft);">
      <span style="font-size: 0.8rem; color: var(--ink-dim); letter-spacing: 0.1em; text-transform: uppercase;">合作单位与认证机构</span>
      <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:32px; margin-top:20px; opacity:0.8;">
        <span style="font-family: var(--font-serif); font-size:1.15rem; color:var(--gold-soft);">彭亨象棋公会</span>
        <span style="font-family: var(--font-serif); font-size:1.15rem; color:var(--gold-soft);">马来西亚象棋总会</span>
        <span style="font-family: var(--font-serif); font-size:1.15rem; color:var(--gold-soft);">SJK(C) Triang</span>
      </div>
    </div>
'''
text = text.replace('</header>', partners_html)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
