import io, re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix public-hero
old_hero = r'\.public-hero \{[^}]+\}'
new_hero = '''.public-hero {
      width: 100%;
      background: var(--navy-900);
      border: 1px solid var(--gold-soft);
      color: #fff;
      border-radius: 16px;
      padding: 40px 24px;
      text-align: center;
      margin-bottom: 24px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
      position: relative;
      overflow: hidden;
      margin-top: 10px;
    }'''
text = re.sub(old_hero, new_hero, text, count=1)

# 2. Fix ph-stat-pill
old_pill = r'\.ph-stat-pill \{[^}]+\}'
new_pill = '''.ph-stat-pill {
      background: rgba(201, 162, 75, 0.1); /* gold-soft at 10% */
      border: 1px solid var(--gold-soft);
      color: var(--gold-soft);
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }'''
text = re.sub(old_pill, new_pill, text, count=1)

# 3. Fix camp-title
old_title = r'\.camp-title \{[^}]+\}'
new_title = '''.camp-title { 
      font-size: 22px; 
      font-weight: 900; 
      margin-bottom: 12px; 
      line-height: 1.3; 
      color: var(--gold); 
      font-family: var(--font-serif); 
    }'''
text = re.sub(old_title, new_title, text, count=1)

# 4. Fix camp-details
old_details = r'\.camp-details \{[^}]+\}'
new_details = '''.camp-details { 
      font-size: 15px; 
      font-weight: 700; 
      opacity: 0.95; 
      margin-bottom: 16px; 
      line-height: 1.6; 
      color: var(--text); 
    }'''
text = re.sub(old_details, new_details, text, count=1)


with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
