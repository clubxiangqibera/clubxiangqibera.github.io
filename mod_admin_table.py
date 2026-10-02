import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update table header if it doesn't have XQF
if '<th>XQF棋谱</th>' not in text:
    text = text.replace('<th>记谱纸</th>', '<th>记谱纸</th><th>XQF棋谱</th>')
    # If the exact string wasn't '<th>记谱纸</th>', let's use a regex
    import re
    text = re.sub(r'(<th>.*?记谱纸.*?</th>)', r'\1<th>XQF棋谱</th>', text)

# 2. Update renderMatchesTable to include XQF upload/download
old_render = """function renderMatchesTable(){
  const el = document.getElementById('matchHistoryTable');
  if (!el) return;
  el.innerHTML=allMatches.slice().reverse().map(m=>{
    const imgBtn=m.recordImg&&m.recordImg.startsWith('http')
      ?`<button class="btn-sm" onclick="openLightbox('${m.recordImg}')">📸 查看</button>`:'-';
    return`<tr><td>${m.date}</td><td>${m.round}</td><td><strong>${m.red}</strong></td><td>${m.result}</td><td><strong>${m.black}</strong></td><td>${m.verdict}</td><td>${imgBtn}</td></tr>`
  }).join('');
}"""

# Actually, the user had "上传实体记谱纸照片" in the card before... wait! 
# In admin.html there is no card view for matches! It's just a table!
# My previous `mod_xqf.py` tried to replace a card view string which didn't exist in admin.html, that's why it failed!

new_render = """function renderMatchesTable(){
  const el = document.getElementById('matchHistoryTable');
  if (!el) return;
  el.innerHTML=allMatches.slice().reverse().map(m=>{
    const imgBtn=m.recordImg&&m.recordImg.startsWith('http')
      ?`<button class="btn-sm" onclick="openLightbox('${m.recordImg}')">📸 查看记谱纸</button>`
      :`<button class="btn-sm" onclick="document.getElementById('matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()">📤 传照片</button>
        <input type="file" id="matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept="image/*" onchange="uploadMatchPhotoFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">`;
        
    const xqfBtn=m.xqfFile&&m.xqfFile.startsWith('http')
      ?`<button class="btn-sm" onclick="window.open('${m.xqfFile}')">💾 下载XQF</button>`
      :`<button class="btn-sm" onclick="document.getElementById('xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()">📤 传XQF</button>
        <input type="file" id="xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept=".xqf" onchange="uploadXqfFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">`;

    return`<tr><td>${m.date}</td><td>${m.round}</td><td><strong>${m.red}</strong></td><td>${m.result}</td><td><strong>${m.black}</strong></td><td>${m.verdict}</td><td>${imgBtn}</td><td>${xqfBtn}</td></tr>`
  }).join('');
}"""

import re
text = re.sub(r'function renderMatchesTable\(\).*?\}\)\.join\(\'\'\);\n\}', new_render, text, flags=re.DOTALL)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("admin.html match table updated")
