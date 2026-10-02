import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix public-hero CSS to match camp-banner
old_hero_css = r'''\.public-hero \{
      width: 100%;
      background: var\(--hero-bg\);
      border: var\(--hero-border\);
      backdrop-filter: var\(--glass-blur\);
      -webkit-backdrop-filter: var\(--glass-blur\);
      color: #fff;
      border-radius: 24px;
      padding: 40px 24px;
      text-align: center;
      margin-bottom: 24px;
      box-shadow: 0 14px 40px rgba\(0,0,0,0\.2\);
    \}'''
new_hero_css = '''.public-hero {
      width: 100%;
      background: var(--navy-900);
      border: 1px solid var(--gold-soft);
      color: #fff;
      border-radius: 16px;
      padding: 40px 24px;
      text-align: center;
      margin-bottom: 24px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }'''
text = re.sub(old_hero_css, new_hero_css, text)

# 2. Fix the ph-stats-grid text
old_stats_html = r'''<div class="ph-stats-grid">
          <div class="ph-stat-pill">👨‍🎓 <span id="statPlayers">25\+</span> 在册学员</div>
          <div class="ph-stat-pill">⚔️ <span id="statMatches">150\+</span> 实战对局</div>
          <div class="ph-stat-pill">🏅 5 级段位考评体系</div>
        </div>'''
new_stats_html = '''<div class="ph-stats-grid">
          <div class="ph-stat-pill">👑 全县唯一象棋教育学院</div>
          <div class="ph-stat-pill">⚔️ CXQB ELO 官方排位</div>
          <div class="ph-stat-pill">🏅 5 级段位考评体系</div>
        </div>'''
text = re.sub(old_stats_html, new_stats_html, text)

# Also remove the span JS updater
text = re.sub(r"const statPlayers = document\.getElementById\('statPlayers'\);", "// removed", text)
text = re.sub(r"const statMatches = document\.getElementById\('statMatches'\);", "// removed", text)
text = re.sub(r"if \(statPlayers\) statPlayers\.textContent = globalStudents\.length \+ '\+';", "// removed", text)
text = re.sub(r"if \(statMatches\) statMatches\.textContent = globalMatches\.length \+ '\+';", "// removed", text)


with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
