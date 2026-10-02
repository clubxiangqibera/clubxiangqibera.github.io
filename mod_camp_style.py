import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update camp-banner CSS
old_css = r'''\.camp-banner \{
      width: 100%;
      background: linear-gradient\(135deg, #F9E79F 0%, #F5CBA7 100%\);
      border-radius: 24px;
      padding: 24px;
      display: flex;
      gap: 24px;
      align-items: center;
      margin-bottom: 24px;
      box-shadow: 0 12px 30px rgba\(243, 156, 18, 0\.2\);
      color: #7D6608;
      border: 1px solid rgba\(255,255,255,0\.6\);
    \}'''

new_css = '''.camp-banner {
      width: 100%;
      background: var(--navy-900);
      border-radius: 16px;
      padding: 32px;
      display: flex;
      gap: 32px;
      align-items: center;
      margin-bottom: 32px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
      color: var(--ink-dim);
      border: 1px solid var(--gold-soft);
    }'''
text = re.sub(old_css, new_css, text)

# 2. Update camp-title CSS
old_title_css = r'''\.camp-title \{
      font-size: 1\.6rem;
      font-weight: 800;
      color: #935116;
      margin-bottom: 12px;
      line-height: 1\.3;
    \}'''

new_title_css = '''.camp-title {
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--gold);
      margin-bottom: 12px;
      line-height: 1.3;
      font-family: var(--font-serif);
    }'''
text = re.sub(old_title_css, new_title_css, text)

# 3. Update the button HTML
old_btn = 'class="btn-wa" style="background:#4285F4;box-shadow: 0 6px 16px rgba(66,133,244,0.3);"'
new_btn = 'class="btn-wa" style="background:#b3262d;box-shadow: 0 6px 16px rgba(179,38,45,0.4); border:none; padding:12px 24px;"'
text = text.replace(old_btn, new_btn)

# 4. Update the badge HTML
old_badge = '<div class="camp-badge">✅ 报名开放中</div>'
# wait, earlier I might have replaced '报名开放中' with a span!
# let's just use regex for the badge background
old_badge_css = r'''\.camp-badge \{
      display: inline-block;
      background: #E74C3C;
      color: white;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 0\.85rem;
      font-weight: bold;
      margin-bottom: 12px;
      box-shadow: 0 4px 10px rgba\(231,76,60,0\.4\);
    \}'''
new_badge_css = '''.camp-badge {
      display: inline-block;
      background: #b3262d;
      color: white;
      padding: 6px 16px;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: bold;
      margin-bottom: 12px;
      box-shadow: 0 4px 10px rgba(179,38,45,0.4);
    }'''
text = re.sub(old_badge_css, new_badge_css, text)


with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
