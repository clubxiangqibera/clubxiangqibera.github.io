import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("verdict:(r[7]||'').trim(),recordImg:(r[8]||'').trim()", "verdict:(r[7]||'').trim(),recordImg:(r[8]||'').trim(),xqfFile:(r[9]||'').trim()")

old_render = """function renderMatchLogList(matches) {
  const c = document.getElementById('matchLogList');
  if (!matches.length) { c.innerHTML = '<p style="text-align:center;color:var(--text2);padding:14px;">暂无对局记录</p>'; return; }
  c.innerHTML = matches.slice().reverse().map(m => {
    const hasImg = m.recordImg && (m.recordImg.startsWith('http') || m.recordImg.startsWith('data:image'));
    const imgBtn = hasImg 
      ? `<button onclick="openLightbox('${m.recordImg}')" style="padding:6px 14px;border-radius:8px;border:1.5px solid var(--border);background:#fff;font-size:12px;font-weight:800;cursor:pointer;">📷 查看真实记谱纸</button>` : '';
    
    let isMyMatch = false;
    if (currentUser && currentUser.role === 'student' && currentUser.data) {
      if (m.red === currentUser.data.cnName || m.black === currentUser.data.cnName) isMyMatch = true;
    }
    const borderStyle = isMyMatch ? "border-left: 5px solid #F1C40F; background: #FFFCF2;" : "";
    const badge = isMyMatch ? '<span style="font-size:11px;background:#F1C40F;color:#7D6608;padding:2px 8px;border-radius:6px;font-weight:900;margin-left:8px;">★ 专属对局</span>' : '';

    return `
      <div class="match-card" style="${borderStyle}">
        <div style="flex:1;">
          <div class="match-title">
            <span>🔴 ${m.red}</span> <span style="color:var(--text2);font-weight:400;font-size:12px;">vs</span> <span>⚫ ${m.black}</span>
            <span style="font-size:12px;font-weight:800;color:var(--primary-mid);margin-left:4px;">${m.result}</span>
            ${badge}
          </div>
          <div class="match-meta">${m.date} · ${m.round} · 判定: ${m.verdict}</div>
        </div>
        <div>${imgBtn}</div>
      </div>
    `;
  }).join('');
}"""

new_render = """function renderMatchLogList(matches) {
  const c = document.getElementById('matchLogList');
  let displayMatches = matches.slice().reverse();
  
  if (currentUser && currentUser.role === 'student' && currentUser.data) {
    displayMatches = displayMatches.filter(m => m.red === currentUser.data.cnName || m.black === currentUser.data.cnName);
  }
  
  if (!displayMatches.length) { 
    c.innerHTML = '<p style="text-align:center;color:var(--text2);padding:14px;">暂无对局记录</p>'; 
    return; 
  }
  
  c.innerHTML = displayMatches.map(m => {
    const hasImg = m.recordImg && (m.recordImg.startsWith('http') || m.recordImg.startsWith('data:image'));
    const imgBtn = hasImg 
      ? `<button onclick="openLightbox('${m.recordImg}')" style="padding:6px 14px;border-radius:8px;border:1.5px solid var(--border);background:#fff;font-size:12px;font-weight:800;cursor:pointer;width:100%;">📸 实体记谱纸</button>` : '';

    const hasXqf = m.xqfFile && m.xqfFile.startsWith('http');
    const xqfBtn = hasXqf 
      ? `<button onclick="window.open('${m.xqfFile}')" style="padding:6px 14px;border-radius:8px;border:1.5px solid var(--border);background:#fff;font-size:12px;font-weight:800;cursor:pointer;margin-top:6px;width:100%;">💾 下载XQF棋谱</button>`
      : (currentUser && currentUser.role === 'student' ? `<button onclick="document.getElementById('xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()" style="padding:6px 14px;border-radius:8px;border:1.5px dashed var(--border);background:var(--bg);font-size:12px;font-weight:800;color:var(--text2);cursor:pointer;margin-top:6px;width:100%;">📤 上传XQF</button>
         <input type="file" id="xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept=".xqf" onchange="uploadXqfFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">` : '');
    
    return `
      <div class="match-card" style="border-left: 5px solid #F1C40F; background: #FFFCF2;">
        <div style="flex:1;">
          <div class="match-title">
            <span>🔴 ${m.red}</span> <span style="color:var(--text2);font-weight:400;font-size:12px;">vs</span> <span>⚫ ${m.black}</span>
            <span style="font-size:12px;font-weight:800;color:var(--primary-mid);margin-left:4px;">${m.result}</span>
          </div>
          <div class="match-meta">${m.date} · ${m.round} · 判定: ${m.verdict}</div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; min-width:120px;">
          ${imgBtn}
          ${xqfBtn}
        </div>
      </div>
    `;
  }).join('');
}"""

if old_render in text:
    text = text.replace(old_render, new_render)
else:
    print("WARNING: renderMatchLogList not found")

js_func = """
async function uploadXqfFile(date, round, redName, blackName, inputEl) {
  if (!inputEl.files || inputEl.files.length === 0) return;
  const file = inputEl.files[0];
  const ogText = inputEl.previousElementSibling.innerHTML;
  inputEl.previousElementSibling.innerHTML = '上传中...';
  
  try {
    const reader = new FileReader();
    reader.onload = async function(e) {
      const base64 = e.target.result;
      const res = await fetch(GAS_API_URL, {
        method: 'POST',
        body: JSON.stringify({ action: 'updateMatchXQF', date: date, round: round, redName: redName, blackName: blackName, fileBase64: base64 })
      });
      const data = await res.json();
      if(data.success) {
        alert('XQF棋谱上传成功！');
        loadMatches(); // Reload matches
      } else {
        alert('上传失败: ' + (data.error||''));
      }
    };
    reader.readAsDataURL(file);
  } catch (e) {
    alert('网络错误');
  }
  inputEl.previousElementSibling.innerHTML = ogText;
  inputEl.value = '';
}
"""
if 'uploadXqfFile' not in text:
    text = text.replace('// --- Public Gallery JS ---', js_func + '\n// --- Public Gallery JS ---')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace("verdict:(r[7]||'').trim(),recordImg:(r[8]||'').trim()", "verdict:(r[7]||'').trim(),recordImg:(r[8]||'').trim(),xqfFile:(r[9]||'').trim()")

# In admin.html, update renderMatchesTable to also show XQF file
admin_old = """const imgBtn=m.recordImg&&m.recordImg.startsWith('http')
      ?`<div onclick="openLightbox('${m.recordImg}')" style="padding:12px;background:#F8F9F9;color:var(--pri3);font-size:12px;font-weight:700;text-align:center;cursor:pointer;border-top:1px solid var(--border);">📸 查看实体记谱纸照片</div>`
      :`<div onclick="document.getElementById('matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()" style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">上传实体记谱纸照片</div>
      <input type="file" id="matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept="image/*" onchange="uploadMatchPhotoFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">`;"""

admin_new = """const imgBtn=m.recordImg&&m.recordImg.startsWith('http')
      ?`<div onclick="openLightbox('${m.recordImg}')" style="padding:12px;background:#F8F9F9;color:var(--pri3);font-size:12px;font-weight:700;text-align:center;cursor:pointer;border-top:1px solid var(--border);">📸 查看实体记谱纸照片</div>`
      :`<div onclick="document.getElementById('matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()" style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">上传实体记谱纸照片</div>
      <input type="file" id="matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept="image/*" onchange="uploadMatchPhotoFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">`;
    
    const xqfBtn=m.xqfFile&&m.xqfFile.startsWith('http')
      ?`<div onclick="window.open('${m.xqfFile}')" style="padding:12px;background:#EBF5FB;color:var(--pri3);font-size:12px;font-weight:700;text-align:center;cursor:pointer;border-top:1px solid var(--border);">💾 下载XQF电子棋谱</div>`
      :`<div style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);">暂无XQF棋谱</div>`;"""

if admin_old in text2:
    text2 = text2.replace(admin_old, admin_new)
    text2 = text2.replace('${imgBtn}\n      </div>', '${imgBtn}\n        ${xqfBtn}\n      </div>')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text2)

print("HTML edits complete")
