
const SHEET_ID = '1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y';
const GAS_API_URL = 'https://script.google.com/macros/s/AKfycbyFY__BC0NXW87ZK1okkzhlskQ4PPBJx2QEXf0-8Icv8tbFHZcRSVge60TqU11DU4v_/exec';
function getAuthPin() {
  const s = localStorage.getItem('cxb_auth');
  return s ? JSON.parse(s).pin : '';
}

let allStudents = [];
let allMatches = [];
let uploadBase64 = null;

function parseCSV(t){const r=[];let w=[],q=!1,c='';for(let i=0;i<t.length;i++){const x=t[i],n=t[i+1];if(x==='"'){q&&n==='"'?(c+='"',i++):q=!q}else if(x===','&&!q){w.push(c);c=''}else if((x==='\r'||x==='\n')&&!q){x==='\r'&&n==='\n'&&i++;w.push(c);w.some(z=>z.trim())&&r.push(w);w=[];c=''}else c+=x}if(c||w.length){w.push(c);w.some(z=>z.trim())&&r.push(w)}return r;}

function checkAuth(){
  const s = localStorage.getItem('cxb_auth');
  if (s) {
    const d = JSON.parse(s);
    if (d.pin && Date.now() - d.ts < 86400000) return true;
  }
  return false;
}

async function tryLogin(){
  const input = document.getElementById('adminPinInput');
  const p = input.value.trim();
  const btn = document.getElementById('aBtn');
  const og = btn.innerHTML;
  btn.innerHTML = '🔄 验证中...';
  btn.disabled = true;

  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ pin: p })
    });
    const data = await res.json();
    if (data.valid) {
      localStorage.setItem('cxb_auth',JSON.stringify({pin:p,ts:Date.now()}));
      localStorage.setItem('cxb_auth_user',JSON.stringify({role: data.role, perms: data.perms || [], name: data.name || ''}));
      showApp();
    } else {
      input.classList.add('error');
      input.value='';
      const err = document.getElementById('loginError');
      err.textContent = data.error || '❌ 密码错误，请重新输入';
      err.style.display='block';
      input.focus();
      setTimeout(()=>input.classList.remove('error'),500);
    }
  } catch (e) {
    const err = document.getElementById('loginError');
    err.textContent = '❌ 网络连接错误，请检查网络';
    err.style.display='block';
  } finally {
    btn.innerHTML = og;
    btn.disabled = false;
  }
}

function setAdminLang(lang) {
  document.getElementById('aLangZh').classList.toggle('active', lang === 'zh');
  document.getElementById('aLangEn').classList.toggle('active', lang === 'en');
  if (lang === 'zh') {
    document.getElementById('aSub').textContent = '管理控制台 · Admin Dashboard';
    document.getElementById('adminPinInput').placeholder = '输入管理密码 (Enter Password)';
    document.getElementById('aBtn').textContent = '🔐 进入管理控制台';
    document.getElementById('loginError').textContent = '❌ 密码错误，请重新输入';
    document.getElementById('aReturn').textContent = '← 返回主页 (Return to Menu)';
  } else {
    document.getElementById('aSub').textContent = 'Admin Dashboard';
    document.getElementById('adminPinInput').placeholder = 'Enter Admin Password';
    document.getElementById('aBtn').textContent = '🔐 Login to Dashboard';
    document.getElementById('loginError').textContent = '❌ Invalid Password';
    document.getElementById('aReturn').textContent = '← Return to Menu';
  }
}

function logout(){
  localStorage.removeItem('cxb_auth');
  localStorage.removeItem('cxb_auth_user');
  window.location.href = 'index.html';
}

function showApp(){
    document.getElementById('loginScreen').style.display='none';
    document.getElementById('mainApp').style.display='block';
    const user = JSON.parse(localStorage.getItem('cxb_auth_user'));
    const isSuperAdmin = user && user.role === 'superadmin';
    const perms = (user && user.perms) || [];

    const tabs = ['dashboard', 'students', 'payments', 'records', 'tournament', 'ladder', 'accounts', 'licenses', 'gallery'];
    tabs.forEach(tab => {
       const tabEl = document.querySelector(`[data-tab="${tab}"]`);
       if (tabEl) {
          const permName = tab === 'records' ? 'matches' : tab;
          if (isSuperAdmin || perms.includes(permName)) {
             tabEl.style.display = 'block';
          } else {
             tabEl.style.display = 'none';
          }
       }
    });

    loadAllData();
  }

function switchTab(t){
  document.querySelectorAll('.nav-tab').forEach(x=>x.classList.toggle('active',x.dataset.tab===t));
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.toggle('active',p.id==='panel-'+t));
  
  if (t === 'licenses') {
    loadSchoolLicenses();
  }
}

async function loadAllData(){
  await Promise.all([loadStudents(), loadMatches()]);
  renderDashboard();
  renderLadder(allStudents);
  renderAccountList();
}

async function loadStudents(){
  try{
    const url=`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent('学员档案总册')}`;
    const res=await fetch(url);const csv=await res.text();const rows=parseCSV(csv);
    allStudents=[];
    for(let i=1;i<rows.length;i++){
      const r=rows[i];const id=(r[0]||'').trim();if(!id)continue;
      allStudents.push({
        id,cnName:(r[1]||'').trim(),enName:(r[2]||'').trim(),
        gender:(r[3]||'').trim(),age:(r[4]||'').trim(),school:(r[5]||'').trim(),
        level:(r[6]||'').trim(),feeMode:(r[7]||'').trim(),payStatus:(r[8]||'').trim(),
        comboExpiry:(r[9]||'').trim(),whatsapp:(r[10]||'').trim(),
        elo:parseInt(r[11])||200,tier:(r[12]||'').trim()
      });
    }
    renderStudentTables();
    renderLadder(allStudents);
  }catch(e){console.error(e);}
}

function getTierName(elo) {
  if (elo >= 1300) return '<span class="tier-chip tier-1">👑 一级棋手</span>';
  if (elo >= 1000) return '<span class="tier-chip tier-2">💎 二级棋手</span>';
  if (elo >= 700) return '<span class="tier-chip tier-3">🥇 三级棋手</span>';
  if (elo >= 400) return '<span class="tier-chip tier-4">🥈 四级棋手</span>';
  return '<span class="tier-chip tier-5">🥉 五级棋手</span>';
}

function getPlayerStats(id, name) {
  let w = 0, d = 0, l = 0;
  allMatches.forEach(m => {
    const isRed = m.redId === id || m.red === name;
    const isBlack = m.blackId === id || m.black === name;
    if (!isRed && !isBlack) return;
    if (m.verdict.includes('胜')) {
      if ((isRed && m.verdict.includes(m.red)) || (isBlack && m.verdict.includes(m.black))) w++;
      else l++;
    } else if (m.verdict.includes('和')) {
      d++;
    }
  });
  const total = w + d + l;
  const wr = total > 0 ? ((w / total) * 100).toFixed(0) : 0;
  return { w, d, l, total, wr };
}

// ── ACCOUNT MANAGER ──────────────────────────────────────────
function getDefaultPwd(student) {
  // Default password = Level digit + ID number, e.g. Lv2 XQB-001 → 2001
  const lvMatch = (student.level || '').match(/Lv\s*(\d)/);
  const lvNum = lvMatch ? lvMatch[1] : '1';
  const idMatch = (student.id || '').match(/(\d+)$/);
  const idNum = idMatch ? idMatch[1] : '000';
  return lvNum + idNum;
}

function renderAccountList() {
  const el = document.getElementById('accountListTable');
  const countEl = document.getElementById('accStudentCount');
  if (!el) return;
  if (countEl) countEl.textContent = `共 ${allStudents.length} 名学员`;

  // Update PIN display in the permission card
  const dispSuper = document.getElementById('displaySuperPin');
  const dispCoach = document.getElementById('displayCoachPin');
  if (dispSuper) dispSuper.textContent = '********';
  if (dispCoach) dispCoach.textContent = '********';

  // Teacher PIN editor removed (moved to coach list UI)
  el.innerHTML = `
    <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="background:var(--bg);border-bottom:2px solid var(--border);">
            <th style="padding:10px 12px;text-align:left;font-weight:800;color:var(--text2);">学号</th>
            <th style="padding:10px 12px;text-align:left;font-weight:800;color:var(--text2);">中文姓名 (账号)</th>
            <th style="padding:10px 12px;text-align:left;font-weight:800;color:var(--text2);">密码 <span style="font-weight:500;color:var(--text2);font-size:11px;">(默认=级别+编号)</span></th>
            <th style="padding:10px 12px;text-align:left;font-weight:800;color:var(--text2);">班级</th>
            <th style="padding:10px 12px;text-align:center;font-weight:800;color:var(--text2);">状态</th>
            <th style="padding:10px 12px;text-align:center;font-weight:800;color:var(--text2);">操作</th>
          </tr>
        </thead>
        <tbody>
          ${allStudents.map((s, i) => {
            const defaultPwd = getDefaultPwd(s);
            const currentPwd = s.password || defaultPwd;
            const isDefault = currentPwd === defaultPwd;
            return `
            <tr style="border-bottom:1px solid var(--border);" onmouseover="this.style.background='var(--bg)'" onmouseout="this.style.background=''">
              <td style="padding:10px 12px;font-weight:700;color:var(--text2);">${s.id}</td>
              <td style="padding:10px 12px;">
                <input type="text" id="acc_name_${i}" value="${s.cnName}"
                  style="width:100%;padding:6px 10px;border:1.5px solid var(--border);border-radius:8px;font-size:13px;font-weight:700;background:var(--bg);transition:border-color .2s;"
                  onfocus="this.style.borderColor='#F39C12'"
                  onblur="autoSaveAccount(${i},'${s.id}',this)">
              </td>
              <td style="padding:10px 12px;">
                <div style="display:flex;align-items:center;gap:6px;">
                  <input type="text" id="acc_pwd_${i}" value="${currentPwd}" maxlength="8"
                    style="width:90px;padding:6px 10px;border:1.5px solid var(--border);border-radius:8px;font-size:13px;font-weight:700;background:var(--bg);transition:border-color .2s;"
                    onfocus="this.style.borderColor='#F39C12'"
                    onblur="autoSaveAccount(${i},'${s.id}',this)">
                  ${isDefault ? '<span style="font-size:10px;background:rgba(41,128,185,0.12);color:#2980B9;padding:2px 6px;border-radius:6px;font-weight:700;">默认</span>' : '<span style="font-size:10px;background:rgba(39,174,96,0.12);color:#27AE60;padding:2px 6px;border-radius:6px;font-weight:700;">已改</span>'}
                </div>
              </td>
              <td style="padding:10px 12px;">
                <select id="acc_level_${i}" 
                  style="width:100%;padding:4px 6px;border:1.5px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg);"
                  onchange="autoSaveAccount(${i},'${s.id}',this)">
                  <option value="Lv 1 启蒙班" ${s.level==='Lv 1 启蒙班'?'selected':''}>Lv 1 启蒙班</option>
                  <option value="Lv 2 进阶班" ${s.level==='Lv 2 进阶班'?'selected':''}>Lv 2 进阶班</option>
                  <option value="Lv 3 精英班" ${s.level==='Lv 3 精英班'?'selected':''}>Lv 3 精英班</option>
                  <option value="非本会学员" ${s.level==='非本会学员'?'selected':''}>非本会学员</option>
                </select>
              </td>
              <td style="padding:10px 12px;text-align:center;" id="acc_status_${i}">
                <span style="font-size:11px;color:var(--text2);">-</span>
              </td>
              <td style="padding:10px 12px;text-align:center;">
                <button onclick="deleteStudentAccount('${s.id}','${s.cnName}')"
                  style="background:none;border:1px solid var(--red);color:var(--red);border-radius:6px;padding:3px 8px;font-size:11px;font-weight:800;cursor:pointer;"
                  onmouseover="this.style.background='var(--red)';this.style.color='#fff';" onmouseout="this.style.background='none';this.style.color='var(--red)';">
                  🗑️ 删除
                </button>
              </td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>`;
}

async function saveCoachPin(newPin) {
  const trimmed = newPin.trim();
  if (!trimmed || trimmed.length < 4) { toast('教练密码至少需要4位！', 'error'); return; }
  
  const input = document.getElementById('coachPinInput');
  if (input) input.style.borderColor = '#F39C12';
  
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/set-coach-pin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), newCoachPin: trimmed })
    });
    const data = await res.json();
    if (data.success) {
      if (input) input.style.borderColor = '#27AE60';
      toast(`✅ 教练密码已同步到云端数据库`, 'success');
      // Hide the actual pin from display
      const disp = document.getElementById('coachPinDisplay');
      if (disp) disp.textContent = '********';
    } else {
      toast('修改失败：' + (data.error || '权限不足'), 'error');
      if (input) input.style.borderColor = '#E74C3C';
    }
  } catch (e) {
    toast('网络连接失败', 'error');
  }
}

async function autoSaveAccount(idx, studentId, inputEl) {
  const newName = document.getElementById(`acc_name_${idx}`).value.trim();
  const newPwd  = document.getElementById(`acc_pwd_${idx}`).value.trim();
  const newLevelEl = document.getElementById(`acc_level_${idx}`);
  const newLevel = newLevelEl ? newLevelEl.value : '';
  if (!newName || !newPwd) return;

  const statusEl = document.getElementById(`acc_status_${idx}`);
  if (statusEl) statusEl.innerHTML = '<span style="font-size:11px;color:#F39C12;">⏳ 保存中...</span>';
  if (inputEl) inputEl.style.borderColor = '#F39C12';

  try {
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'updateAccount', studentId, newName, newPwd, newLevel })
    });
    const data = await res.json();
    if (data.status === 'ok') {
      if (statusEl) statusEl.innerHTML = '<span style="font-size:11px;color:#27AE60;">✅ 已保存</span>';
      if (inputEl) inputEl.style.borderColor = '#27AE60';
      setTimeout(() => { if (statusEl) statusEl.innerHTML = '<span style="font-size:11px;color:var(--text2);">-</span>'; }, 3000);
    } else {
      if (statusEl) statusEl.innerHTML = '<span style="font-size:11px;color:#E74C3C;">⚠️ 失败</span>';
      if (inputEl) inputEl.style.borderColor = '#E74C3C';
    }
  } catch(e) {
    if (statusEl) statusEl.innerHTML = '<span style="font-size:11px;color:#E74C3C;">⚠️ 离线</span>';
    if (inputEl) inputEl.style.borderColor = '#E74C3C';
  }
}

function renderLadder(players) {
  const p = [...players].sort((a,b)=>b.elo - a.elo);
  const area = document.getElementById('podiumArea');
  if (!area) return;
  const top3 = p.slice(0,3);
  let ph = '';
  top3.forEach((pl, i) => {
    let cls = i===0 ? 'pod-1' : (i===1 ? 'pod-2' : 'pod-3');
    let med = i===0 ? '🥇' : (i===1 ? '🥈' : '🥉');
    let extra = i===0 ? '<div class="crown">⭐ 首席榜首</div>' : '';
    const st = getPlayerStats(pl.id, pl.cnName);
    ph += `<div class="pod ${cls}">${extra}<div class="pod-medal">${med}</div><div class="pod-name">${pl.cnName}</div><div class="pod-school">${pl.school}</div>${getTierName(pl.elo)}<div class="pod-elo">${pl.elo}</div><div class="pod-stats">${st.w}胜 ${st.d}和 ${st.l}负</div></div>`;
  });
  area.innerHTML = ph;

  const rl = document.getElementById('rankList');
  if (!rl) return;
  rl.innerHTML = p.map((pl, i) => {
    let n = i+1;
    let nHTML = n<=3 ? `<span style="color:${n===1?'#F1C40F':n===2?'#BDC3C7':'#EDBB99'}">${n}</span>` : n;
    const st = getPlayerStats(pl.id, pl.cnName);
    return `<div class="rank-card"><div class="rank-left"><div class="rank-num">${nHTML}</div><div class="rank-info"><div class="rank-name">${pl.cnName} ${getTierName(pl.elo)}</div><div class="rank-school">${pl.school} · ${st.total} 场实战 (${st.w}胜 ${st.d}和 ${st.l}负)</div></div></div><div class="rank-right"><div class="rank-elo">${pl.elo}</div><div class="rank-wr">胜率 ${st.wr}%</div></div></div>`;
  }).join('');
}

async function loadMatches(){
  try{
    const url=`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent('实战对局记录表')}`;
    const res=await fetch(url);const csv=await res.text();const rows=parseCSV(csv);
    allMatches=[];
    for(let i=1;i<rows.length;i++){
      const r=rows[i];const date=(r[0]||'').trim();if(!date)continue;
      allMatches.push({
        date,round:(r[1]||'').trim(),redId:(r[2]||'').trim(),red:(r[3]||'').trim(),
        result:(r[4]||'').trim(),blackId:(r[5]||'').trim(),black:(r[6]||'').trim(),
        verdict:(r[7]||'').trim(),recordImg:(r[8]||'').trim()
      });
    }
    renderMatchesTable();
    renderGallery();
  }catch(e){console.error(e);}
}

function payBadge(s){
  if(s.includes('已缴费')||s.includes('Verified'))return'<span class="badge badge-green">✅ 已缴费</span>';
  return'<span class="badge badge-yellow">⏳ 待缴费</span>';
}

function renderDashboard(){
  document.getElementById('sTotalStudents').textContent=allStudents.length;
  const p=allStudents.filter(s=>!s.payStatus.includes('已缴费')&&!s.payStatus.includes('Verified')).length;
  document.getElementById('sPending').textContent=p;
  document.getElementById('sMatches').textContent=allMatches.length;

  let rev=0;
  allStudents.forEach(s=>{
    if(s.level.includes('Lv 1'))rev+=70;else if(s.level.includes('Lv 2'))rev+=85;else rev+=110;
  });
  document.getElementById('sRevenue').textContent='RM '+rev;

  document.getElementById('dashStudentTable').innerHTML=allStudents.map(s=>
    `<tr><td><strong>${s.id}</strong></td><td>${s.cnName}</td><td>${s.school}</td><td><span class="badge badge-blue">${s.level}</span></td><td><strong>${s.elo}</strong></td><td>${payBadge(s.payStatus)}</td></tr>`
  ).join('');
}

function renderStudentTables(){
  document.getElementById('studentTable').innerHTML=allStudents.map(s=>
    `<tr>
      <td><strong>${s.id}</strong></td>
      <td><strong>${s.cnName}</strong></td>
      <td>${s.enName||'-'}</td>
      <td>${s.gender}</td>
      <td>${s.school}</td>
      <td><span class="badge badge-blue">${s.level}</span></td>
      <td>${s.elo}</td>
      <td>${payBadge(s.payStatus)}</td>
      <td style="text-align:center;">
        <button class="btn-sm" style="color:var(--red);border-color:var(--red);padding:4px 8px;font-size:11px;" onclick="deleteStudentAccount('${s.id}','${s.cnName}')">🗑️ 移除</button>
      </td>
    </tr>`
  ).join('');

  document.getElementById('paymentTable').innerHTML=allStudents.map(s=>
    `<tr><td><strong>${s.id}</strong></td><td>${s.cnName}</td><td>${s.level}</td><td>${s.feeMode}</td><td>${s.comboExpiry||'-'}</td><td>${payBadge(s.payStatus)}</td>
      <td><button class="btn-sm green" onclick="markPaid('${s.id}')">核准已缴</button></td></tr>`
  ).join('');
}

function renderMatchesTable(){
  const el = document.getElementById('matchHistoryTable');
  if (!el) return;
  el.innerHTML=allMatches.slice().reverse().map(m=>{
    const imgBtn=m.recordImg&&m.recordImg.startsWith('http')
      ?`<button class="btn-sm" onclick="openLightbox('${m.recordImg}')">📷 查看</button>`:'-';
    return`<tr><td>${m.date}</td><td>${m.round}</td><td><strong>${m.red}</strong></td><td>${m.result}</td><td><strong>${m.black}</strong></td><td>${m.verdict}</td><td>${imgBtn}</td></tr>`;
  }).join('');
}

function renderGallery(){
  const g=document.getElementById('recordsGallery');
  if (!allMatches.length) {
    g.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--text2);background:var(--card);border-radius:14px;border:1px dashed var(--border);">暂无实战对局记录，尚无已录入比赛！</div>';
    return;
  }
  g.innerHTML=allMatches.slice().reverse().map((m, idx)=>{
    const hasImg=m.recordImg&&(m.recordImg.startsWith('http')||m.recordImg.startsWith('data:image'));
    const img=hasImg?`<img src="${m.recordImg}" onclick="openLightbox('${m.recordImg}')" style="width:100%;height:150px;object-fit:cover;cursor:pointer;border-top:1px solid var(--border);">`
      :`<div style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);">暂无实体记谱纸照片</div>`;
    return `
      <div style="background:var(--card);border-radius:14px;border:1px solid var(--border);overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;justify-content:space-between;">
        <div style="padding:12px 14px;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div style="font-size:11px;color:var(--text2);">${m.date} · ${m.round}</div>
            <button onclick="deleteSingleMatch('${m.date}','${m.round}','${m.red}','${m.black}')"
              style="background:none;border:none;color:var(--red);cursor:pointer;font-size:13px;padding:2px 6px;border-radius:6px;"
              title="删除此盘对局" onmouseover="this.style.background='rgba(231,76,60,0.1)'" onmouseout="this.style.background='none'">
              🗑️
            </button>
          </div>
          <div style="font-weight:900;font-size:14px;margin-top:4px;">🔴 ${m.red} vs ⚫ ${m.black}</div>
          <div style="font-size:12px;color:var(--pri2);font-weight:800;margin-top:2px;">${m.result} · ${m.verdict}</div>
        </div>
        ${img}
      </div>
    `;
  }).join('');
}

function updateFeeOptions() {
  const level = document.getElementById('qLevel').value;
  const feeSelect = document.getElementById('qFee');
  feeSelect.innerHTML = ''; // clear options
  
  if (level.includes('Lv 1')) {
    feeSelect.add(new Option('Combo 季度 (RM200)', 'Combo 季度 (RM200)'));
    feeSelect.add(new Option('月缴 (RM70)', '月缴 (RM70)'));
  } else if (level.includes('Lv 2')) {
    feeSelect.add(new Option('Combo 季度 (RM250)', 'Combo 季度 (RM250)'));
    feeSelect.add(new Option('月缴 (RM85)', '月缴 (RM85)'));
  } else if (level.includes('Lv 3')) {
    feeSelect.add(new Option('Combo 季度 (RM300)', 'Combo 季度 (RM300)'));
    feeSelect.add(new Option('月缴 (RM110)', '月缴 (RM110)'));
  }
}

function pickSchool(s){document.getElementById('qSchool').value=s;}

async function submitFastStudent(){
  const cn=document.getElementById('qName').value.trim();
  const school=document.getElementById('qSchool').value.trim();
  if(!cn||!school){toast('请至少填写姓名与学校！','error');return;}

  toast('⏳ 正在分配学号并入库建档...','info');
  try{
    const payload={
      action:'addStudent',pin: getAuthPin(),cnName:cn,
      enName:document.getElementById('qEn').value.trim(),
      school,level:document.getElementById('qLevel').value,
      feeMode:document.getElementById('qFee').value,
      whatsapp:document.getElementById('qPhone').value.trim()
    };
    const res=await fetch(GAS_API_URL,{method:'POST',body:JSON.stringify(payload)});
    const d=await res.json();
    if(d.success){
      toast(`🎉 ${cn} (${d.newId}) 已成功入库并建档！`,'success');
      document.getElementById('qName').value='';
      await loadAllData();
    }else{
      toast('建档失败: '+(d.error||''),'error');
    }
  }catch(e){toast('网络错误: '+e.message,'error');}
}

async function markPaid(id){
  toast('⏳ 正在同步更新缴费状态...','info');
  try{
    const res=await fetch(GAS_API_URL,{method:'POST',body:JSON.stringify({action:'updatePayment',pin: getAuthPin(),studentId:id,status:'已缴费 (Verified)'})});
    const d=await res.json();
    if(d.success){
      toast(`✅ 学员 ${id} 缴费状态已核准！`,'success');
      await loadAllData();
    }
  }catch(e){toast('更新失败','error');}
}

function copyAcc(){
  navigator.clipboard.writeText('3246504527');
  toast('✅ 银行账号 3246504527 已复制！','success');
}

function openLightbox(s){document.getElementById('lightboxImg').src=s;document.getElementById('lightbox').classList.add('show');}
function toast(m,t='info'){
  const c=document.getElementById('toastContainer');const el=document.createElement('div');
  el.className='toast '+t;el.textContent=m;c.appendChild(el);
  setTimeout(()=>{el.style.opacity='0';setTimeout(()=>el.remove(),300);},3500);
}

const mDateEl = document.getElementById('mDate'); if (mDateEl) mDateEl.valueAsDate = new Date();
if(checkAuth())showApp();

// ============================================================
//  🏆 TOURNAMENT & SP98 SYSTEM (Swiss-System Engine + Batch Import)
// ============================================================
let tournaments = JSON.parse(localStorage.getItem('cxb_tournaments') || '[]');
let currentTournament = null;
let currentViewingRound = 0; // 0-indexed round viewing in manager
let parsedSP98Matches = [];

function saveTournaments() {
  localStorage.setItem('cxb_tournaments', JSON.stringify(tournaments));
}

// --- Sub-Tab Switching (Engine vs Batch) ---
function switchTourneySubTab(tab) {
  const engSec = document.getElementById('tourneyEngineSection');
  const batSec = document.getElementById('tourneyBatchSection');
  const btnEng = document.getElementById('btnTourneyEngine');
  const btnBat = document.getElementById('btnTourneyBatch');

  if (tab === 'engine') {
    if (engSec) engSec.style.display = 'block';
    if (batSec) batSec.style.display = 'none';
    if (btnEng) { btnEng.classList.add('active'); btnEng.style.background = 'var(--pri)'; btnEng.style.color = '#fff'; }
    if (btnBat) { btnBat.classList.remove('active'); btnBat.style.background = 'var(--bg)'; btnBat.style.color = 'var(--text)'; }
  } else {
    if (engSec) engSec.style.display = 'none';
    if (batSec) batSec.style.display = 'block';
    if (btnBat) { btnBat.classList.add('active'); btnBat.style.background = 'var(--pri)'; btnBat.style.color = '#fff'; }
    if (btnEng) { btnEng.classList.remove('active'); btnEng.style.background = 'var(--bg)'; btnEng.style.color = 'var(--text)'; }
  }
}

// --- Modal for Creating Tournament ---
async function showCreateModal() {
  const list = document.getElementById('tPlayerList');
  const nameInput = document.getElementById('tName');

  // Auto-fill a friendly default tournament name if empty
  if (nameInput && !nameInput.value.trim()) {
    const todayStr = new Date().toISOString().split('T')[0];
    nameInput.value = `CXQB (Club XiangQi Bera) 比赛 (${todayStr})`;
  }

  // If students not loaded yet, fetch immediately
  if (!allStudents.length) {
    list.innerHTML = '<div style="color:var(--text2);padding:10px;">⏳ 正在读取学员名单...</div>';
    await loadStudents();
  }

  if (!allStudents.length) {
    list.innerHTML = '<div style="color:var(--red);padding:10px;">暂未获取到学员数据，请检查网络或重新刷新页面。</div>';
  } else {
    list.innerHTML = allStudents.map(s =>
      `<label class="player-check" style="display:flex;align-items:center;gap:8px;padding:6px 0;cursor:pointer;">
        <input type="checkbox" class="t-player-cb" value="${s.id}" checked>
        <span style="font-weight:700;">${s.cnName}</span>
        <span style="font-size:12px;color:var(--text2);">(${s.id} · ELO ${s.elo})</span>
      </label>`
    ).join('');
  }

  updatePlayerCount();
  document.getElementById('createTournamentModal').classList.add('show');
}

function hideCreateModal() {
  document.getElementById('createTournamentModal').classList.remove('show');
}

function selectAllPlayers() {
  document.querySelectorAll('.t-player-cb').forEach(cb => cb.checked = true);
  updatePlayerCount();
}

function updatePlayerCount() {
  const n = document.querySelectorAll('.t-player-cb:checked').length;
  const countEl = document.getElementById('tPlayerCount');
  if (countEl) countEl.textContent = n;
}

document.addEventListener('change', e => {
  if (e.target && e.target.classList && e.target.classList.contains('t-player-cb')) {
    updatePlayerCount();
  }
});

// --- Create Tournament ---
function createTournament() {
  let name = document.getElementById('tName').value.trim();
  const totalRounds = parseInt(document.getElementById('tRounds').value) || 4;
  const checked = document.querySelectorAll('.t-player-cb:checked');

  if (!name) {
    const todayStr = new Date().toISOString().split('T')[0];
    name = `CXQB (Club XiangQi Bera) 比赛 (${todayStr})`;
  }

  if (checked.length < 2) {
    toast('至少需要勾选 2 名参赛棋手！请在列表勾选选手。', 'error');
    return;
  }

  const players = [];
  checked.forEach(cb => {
    const s = allStudents.find(x => x.id === cb.value);
    if (s) {
      players.push({
        id: s.id,
        name: s.cnName,
        elo: parseInt(s.elo) || 200,
        scores: [],
        opponents: [],
        colors: [],
        hadBye: false
      });
    }
  });

  const t = {
    id: 'T' + Date.now(),
    name,
    totalRounds,
    currentRound: 0,
    status: 'active', // 'active' or 'completed'
    players,
    rounds: [],
    createdAt: new Date().toISOString().split('T')[0]
  };

  tournaments.push(t);
  saveTournaments();
  hideCreateModal();
  toast(`🏆 比赛 "${name}" 已成功创建！`, 'success');

  currentTournament = t;
  startNextRound();
  showTournamentManage();
}

// --- Swiss Pairing Algorithm (SP98 FIDE Engine) ---
function getPlayerTotalPoints(player) {
  if (!player.scores || !player.scores.length) return 0;
  return player.scores.reduce((a, b) => a + b, 0);
}

function swissPair(tournament) {
  const roundNum = tournament.currentRound + 1; // 1-indexed next round
  let activePlayers = [...tournament.players];
  const allPairings = [];

  // Sort players by total tournament score desc, then ELO desc
  activePlayers.sort((a, b) => {
    const sa = getPlayerTotalPoints(a);
    const sb = getPlayerTotalPoints(b);
    return sb - sa || b.elo - a.elo;
  });

  // Handle BYE for odd number of players
  let byePlayer = null;
  if (activePlayers.length % 2 === 1) {
    // Pick the lowest ranked player who hasn't received a bye yet
    for (let i = activePlayers.length - 1; i >= 0; i--) {
      if (!activePlayers[i].hadBye) {
        byePlayer = activePlayers.splice(i, 1)[0];
        break;
      }
    }
    // If all had a bye, pick lowest
    if (!byePlayer) {
      byePlayer = activePlayers.pop();
    }
  }

  // Group remaining players by score brackets
  const brackets = {};
  activePlayers.forEach(p => {
    const sc = getPlayerTotalPoints(p);
    if (!brackets[sc]) brackets[sc] = [];
    brackets[sc].push(p);
  });

  // Score keys descending
  const sortedScoreKeys = Object.keys(brackets).map(Number).sort((a, b) => b - a);

  // Pool for pairing with downfloater carry-over
  let carryOver = [];
  const pairedPlayerIds = new Set();

  sortedScoreKeys.forEach(scKey => {
    let group = [...carryOver, ...brackets[scKey]];
    carryOver = [];

    // Sort group by ELO descending
    group.sort((a, b) => b.elo - a.elo);

    // If odd number in this bracket, float the lowest player to next bracket
    if (group.length % 2 === 1) {
      carryOver.push(group.pop());
    }

    // SP98 Dutch Pairing: Split group into top half and bottom half
    const half = Math.floor(group.length / 2);
    const topHalf = group.slice(0, half);
    let bottomHalf = group.slice(half);

    for (let i = 0; i < topHalf.length; i++) {
      const p1 = topHalf[i];
      let matchIdx = -1;

      // Find an opponent in bottomHalf who p1 hasn't played yet
      for (let j = 0; j < bottomHalf.length; j++) {
        if (!p1.opponents.includes(bottomHalf[j].id)) {
          matchIdx = j;
          break;
        }
      }

      // If everyone in bottomHalf has played p1, try first available
      if (matchIdx === -1 && bottomHalf.length > 0) {
        matchIdx = 0;
      }

      if (matchIdx !== -1) {
        const p2 = bottomHalf.splice(matchIdx, 1)[0];
        pairedPlayerIds.add(p1.id);
        pairedPlayerIds.add(p2.id);

        // Determine colors (alternate based on last color)
        const p1LastColor = p1.colors && p1.colors.length ? p1.colors[p1.colors.length - 1] : null;
        let red, black;
        if (p1LastColor === 'red') {
          red = p2; black = p1;
        } else if (p1LastColor === 'black') {
          red = p1; black = p2;
        } else {
          // Round 1 or no color: higher seed gets red on odd boards
          if ((allPairings.length + 1) % 2 === 1) {
            red = p1; black = p2;
          } else {
            red = p2; black = p1;
          }
        }

        allPairings.push({
          board: allPairings.length + 1,
          redId: red.id,
          redName: red.name,
          blackId: black.id,
          blackName: black.name,
          result: null
        });
      }
    }

    // Any remaining in bottomHalf float to carryOver
    if (bottomHalf.length > 0) {
      carryOver.push(...bottomHalf);
    }
  });

  // Handle any remaining carryOver (if any)
  if (carryOver.length >= 2) {
    for (let k = 0; k < carryOver.length - 1; k += 2) {
      allPairings.push({
        board: allPairings.length + 1,
        redId: carryOver[k].id,
        redName: carryOver[k].name,
        blackId: carryOver[k + 1].id,
        blackName: carryOver[k + 1].name,
        result: null
      });
    }
  }

  // Append bye pairing if applicable
  if (byePlayer) {
    allPairings.push({
      board: 'BYE',
      redId: byePlayer.id,
      redName: byePlayer.name,
      blackId: null,
      blackName: '轮空 (BYE)',
      result: 'bye'
    });
  }

  return allPairings;
}

// --- Start Next Round ---
function startNextRound() {
  const t = currentTournament;
  if (!t || t.currentRound >= t.totalRounds) return;

  const nextPairings = swissPair(t);
  t.currentRound++;
  t.rounds.push({
    roundNum: t.currentRound,
    confirmed: false,
    pairings: nextPairings
  });

  currentViewingRound = t.currentRound - 1;
  saveTournaments();
}

// --- Set Match Result ---
function setMatchResult(roundIdx, boardIdx, result) {
  const t = currentTournament;
  if (!t || !t.rounds[roundIdx]) return;
  if (t.rounds[roundIdx].confirmed) {
    toast('该轮次赛果已确认，无法修改。', 'warning');
    return;
  }
  t.rounds[roundIdx].pairings[boardIdx].result = result;
  saveTournaments();
  renderTournamentManage();
}

// --- Confirm Round ---
function confirmRound() {
  const t = currentTournament;
  if (!t) return;
  const roundIdx = t.currentRound - 1;
  const roundObj = t.rounds[roundIdx];
  if (!roundObj) return;

  // Verify all boards filled
  const unassigned = roundObj.pairings.filter(p => p.result === null);
  if (unassigned.length > 0) {
    toast(`还有 ${unassigned.length} 盘对局未录入赛果，请点击胜负后再确认！`, 'error');
    return;
  }

  // Apply scores and history to players for this round
  roundObj.pairings.forEach(p => {
    if (p.result === 'bye') {
      const byeP = t.players.find(x => x.id === p.redId);
      if (byeP) {
        byeP.hadBye = true;
        byeP.scores.push(1);
        byeP.opponents.push('BYE');
        byeP.colors.push('none');
      }
    } else {
      const redP = t.players.find(x => x.id === p.redId);
      const blackP = t.players.find(x => x.id === p.blackId);

      if (redP) {
        redP.opponents.push(p.blackId);
        redP.colors.push('red');
      }
      if (blackP) {
        blackP.opponents.push(p.redId);
        blackP.colors.push('black');
      }

      if (p.result === 'red') {
        if (redP) redP.scores.push(1);
        if (blackP) blackP.scores.push(0);
      } else if (p.result === 'black') {
        if (redP) redP.scores.push(0);
        if (blackP) blackP.scores.push(1);
      } else {
        if (redP) redP.scores.push(0.5);
        if (blackP) blackP.scores.push(0.5);
      }
    }
  });

  roundObj.confirmed = true;
  saveTournaments();

  if (t.currentRound < t.totalRounds) {
    startNextRound();
    toast(`✅ 第 ${t.currentRound - 1} 轮已锁定，已自动生成第 ${t.currentRound} 轮配对！`, 'success');
  } else {
    toast('🏁 全部轮次已赛完！请点击下方「结束比赛 & 同步云端 ELO」进行积分结算。', 'success');
  }

  renderTournamentManage();
}

// --- Calculate Standings & Buchholz ---
function calculateStandings(tournament) {
  const standings = tournament.players.map(p => {
    const totalPoints = getPlayerTotalPoints(p);
    let buchholz = 0;
    (p.opponents || []).forEach(oppId => {
      if (oppId === 'BYE') return;
      const opp = tournament.players.find(x => x.id === oppId);
      if (opp) buchholz += getPlayerTotalPoints(opp);
    });
    return { ...p, totalPoints, buchholz };
  });

  standings.sort((a, b) => b.totalPoints - a.totalPoints || b.buchholz - a.buchholz || b.elo - a.elo);
  return standings;
}

// --- Tournament Views Navigation ---
function showTournamentList() {
  const listView = document.getElementById('tournamentListView');
  const manageView = document.getElementById('tournamentManageView');
  if (listView) listView.style.display = 'block';
  if (manageView) manageView.style.display = 'none';

  const el = document.getElementById('tournamentCards');
  if (!el) return;

  if (tournaments.length === 0) {
    el.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text2);background:var(--card);border-radius:14px;border:1px dashed var(--border);">暂无比赛记录。点击右上角「+ 创建新比赛」开始！</div>';
    return;
  }

  el.innerHTML = tournaments.slice().reverse().map(t => {
    const statusBadge = t.status === 'completed'
      ? '<span class="badge badge-green">✅ 已结束</span>'
      : `<span class="badge badge-blue">🟢 比赛进行中 (第 ${t.currentRound}/${t.totalRounds} 轮)</span>`;
    return `
      <div class="tournament-card" style="background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px 20px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
        <div>
          <h4 style="font-size:16px;font-weight:900;color:var(--pri);margin-bottom:4px;">🏆 ${t.name}</h4>
          <div style="font-size:12px;color:var(--text2);">📅 ${t.createdAt} · 赛程 ${t.totalRounds} 轮 · ${t.players.length} 名棋手 ${statusBadge}</div>
        </div>
        <div style="display:flex;gap:8px;">
          <button class="btn-sm" style="font-weight:800;" onclick="openTournament('${t.id}')">${t.status === 'completed' ? '查看战绩榜' : '继续对战管理'} →</button>
          <button class="btn-sm" style="color:var(--red);border-color:var(--red);" onclick="deleteTournament('${t.id}')">🗑️ 删除</button>
        </div>
      </div>`;
  }).join('');
}

function openTournament(id) {
  currentTournament = tournaments.find(t => t.id === id);
  if (!currentTournament) return;
  currentViewingRound = Math.max(0, currentTournament.currentRound - 1);
  showTournamentManage();
}

function closeTournamentManage() {
  currentTournament = null;
  showTournamentList();
}

function showTournamentManage() {
  const listView = document.getElementById('tournamentListView');
  const manageView = document.getElementById('tournamentManageView');
  if (listView) listView.style.display = 'none';
  if (manageView) manageView.style.display = 'block';
  renderTournamentManage();
}

function selectViewingRound(idx) {
  currentViewingRound = idx;
  renderTournamentManage();
}

function deleteTournament(id) {
  if (!confirm('确定删除这场比赛记录吗？此操作无法撤销。')) return;
  tournaments = tournaments.filter(t => t.id !== id);
  saveTournaments();
  showTournamentList();
  toast('比赛记录已删除', 'info');
}

// --- Render Tournament Management View ---

function uploadTourneyImg(rIdx, bIdx, input) {
  if (!input.files || !input.files[0]) return;
  const file = input.files[0];
  const reader = new FileReader();
  const statusSpan = document.getElementById(`t_img_status_${rIdx}_${bIdx}`);
  if (statusSpan) statusSpan.innerHTML = '<span style="color:#F39C12;">⏳ 读取中...</span>';
  reader.onload = function(e) {
    if (currentTournament && currentTournament.rounds[rIdx] && currentTournament.rounds[rIdx].pairings[bIdx]) {
      currentTournament.rounds[rIdx].pairings[bIdx].recordImage = e.target.result;
      saveTournaments();
      if (statusSpan) statusSpan.innerHTML = '✅ 已附图';
    }
  };
  reader.readAsDataURL(file);
}

function renderTournamentManage() {
  const t = currentTournament;
  if (!t) return;

  document.getElementById('manageTitle').textContent = `🏆 ${t.name}`;

  // Status badge
  const statusEl = document.getElementById('tourneyStatusBadge');
  if (statusEl) {
    statusEl.innerHTML = t.status === 'completed'
      ? '<span class="badge badge-green" style="font-size:13px;padding:6px 14px;">✅ 比赛已完赛并结算 ELO</span>'
      : `<span class="badge badge-blue" style="font-size:13px;padding:6px 14px;">🟢 正在进行第 ${t.currentRound} / ${t.totalRounds} 轮</span>`;
  }

  // Round Timeline
  const timeline = document.getElementById('roundTimeline');
  let tlHTML = '<div class="round-line"></div>';
  for (let i = 1; i <= t.totalRounds; i++) {
    const rObj = t.rounds[i - 1];
    let cls = 'round-dot';
    if (rObj && rObj.confirmed) cls += ' completed';
    else if (i === t.currentRound) cls += ' active';
    if (i - 1 === currentViewingRound) cls += ' current-viewing';

    tlHTML += `<div class="${cls}" onclick="selectViewingRound(${i - 1})" style="cursor:pointer;" title="点击切换查看第 ${i} 轮">R${i}</div>`;
  }
  timeline.innerHTML = tlHTML;

  // Pairings Section
  const viewRound = t.rounds[currentViewingRound];
  const pHeading = document.getElementById('pairingsHeading');
  const pProgText = document.getElementById('roundProgressText');
  const pList = document.getElementById('pairingsList');
  const confirmBtn = document.getElementById('confirmRoundBtn');
  const endBtn = document.getElementById('endTournamentBtn');

  if (pHeading) pHeading.textContent = `⚔️ 第 ${currentViewingRound + 1} 轮对阵名单`;

  if (!viewRound) {
    pList.innerHTML = '<div style="padding:20px;color:var(--text2);text-align:center;">此轮次尚未配对。</div>';
    if (confirmBtn) confirmBtn.style.display = 'none';
    if (endBtn) endBtn.style.display = 'none';
    return;
  }

  if (pProgText) {
    pProgText.innerHTML = viewRound.confirmed
      ? '<span style="color:var(--green);font-weight:900;">✅ 本轮赛果已锁定</span>'
      : '<span style="color:var(--yellow);font-weight:900;">⏳ 请点选本轮每盘赛果</span>';
  }

  pList.innerHTML = viewRound.pairings.map((p, bIdx) => {
    if (p.result === 'bye') {
      return `
        <div class="board-row" style="background:var(--bg);border-radius:12px;padding:12px 16px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;">
          <div style="font-weight:800;color:var(--pri3);">💤 轮空 (BYE)</div>
          <div style="font-weight:900;color:var(--text);">${p.redName}</div>
          <div style="font-size:12px;font-weight:800;color:var(--green);background:rgba(39,174,96,0.12);padding:4px 10px;border-radius:8px;">+1.0 分</div>
        </div>`;
    }

    const rSel = p.result === 'red' ? 'selected r-red' : '';
    const dSel = p.result === 'draw' ? 'selected r-draw' : '';
    const bSel = p.result === 'black' ? 'selected r-black' : '';

    const redPlayer = t.players.find(x => x.id === p.redId);
    const blackPlayer = t.players.find(x => x.id === p.blackId);
    const redSc = redPlayer ? getPlayerTotalPoints(redPlayer) : 0;
    const blackSc = blackPlayer ? getPlayerTotalPoints(blackPlayer) : 0;

    return `
      <div class="board-row" style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--text2);margin-bottom:8px;">
          <span><strong>台次 ${p.board}</strong></span>
          <span>第 ${currentViewingRound + 1} 轮</span>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;font-size:15px;font-weight:900;">
          <div style="color:var(--red);flex:1;text-align:left;">
            🔴 ${p.redName} <span style="font-size:12px;color:var(--text2);font-weight:600;">(${redSc.toFixed(1)}分 · ${redPlayer ? redPlayer.elo : ''})</span>
          </div>
          <div style="font-size:12px;color:var(--text2);padding:0 10px;">VS</div>
          <div style="color:var(--pri);flex:1;text-align:right;">
            <span style="font-size:12px;color:var(--text2);font-weight:600;">(${blackPlayer ? blackPlayer.elo : ''} · ${blackSc.toFixed(1)}分)</span> ${p.blackName} ⚫
          </div>
        </div>
        <div class="result-btn-group" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          <div style="grid-column:1/-1;text-align:center;font-size:12px;margin-bottom:4px;">
             <label style="cursor:pointer;color:var(--pri2);text-decoration:underline;">
                📎 附加对局记谱纸/照片
                <input type="file" style="display:none;" accept="image/*" onchange="uploadTourneyImg(${currentViewingRound}, ${bIdx}, this)">
             </label>
             <span id="t_img_status_${currentViewingRound}_${bIdx}" style="margin-left:8px;color:#27AE60;font-weight:bold;">
               ${p.recordImage ? '✅ 已附图' : ''}
             </span>
          </div>
          <button class="result-btn ${rSel}" style="${viewRound.confirmed ? 'pointer-events:none;opacity:0.85;' : ''}" onclick="setMatchResult(${currentViewingRound},${bIdx},'red')">🔴 红胜</button>
          <button class="result-btn ${dSel}" style="${viewRound.confirmed ? 'pointer-events:none;opacity:0.85;' : ''}" onclick="setMatchResult(${currentViewingRound},${bIdx},'draw')">🤝 和棋</button>
          <button class="result-btn ${bSel}" style="${viewRound.confirmed ? 'pointer-events:none;opacity:0.85;' : ''}" onclick="setMatchResult(${currentViewingRound},${bIdx},'black')">⚫ 黑胜</button>
        </div>
      </div>`;
  }).join('');

  // Control Buttons Visibility
  const isCurrentActiveRound = currentViewingRound === t.currentRound - 1;
  const isLastRound = t.currentRound === t.totalRounds;

  if (t.status === 'completed') {
    if (confirmBtn) confirmBtn.style.display = 'none';
    if (endBtn) endBtn.style.display = 'none';
  } else if (isCurrentActiveRound && !viewRound.confirmed) {
    if (confirmBtn) {
      confirmBtn.style.display = 'block';
      confirmBtn.textContent = `✅ 确认第 ${t.currentRound} 轮赛果并生成下轮对阵`;
    }
    if (endBtn) endBtn.style.display = 'none';
  } else if (isCurrentActiveRound && viewRound.confirmed && isLastRound) {
    if (confirmBtn) confirmBtn.style.display = 'none';
    if (endBtn) {
      endBtn.style.display = 'block';
      endBtn.textContent = '🏁 结束比赛 & 同步云端 ELO (K-Factor 结算)';
    }
  } else {
    if (confirmBtn) confirmBtn.style.display = 'none';
    if (endBtn) endBtn.style.display = 'none';
  }

  // Standings Table
  const standings = calculateStandings(t);
  const sHead = document.getElementById('standingsHead');
  let hHTML = '<tr><th style="padding:10px;">排名</th><th style="padding:10px;text-align:left;">姓名</th>';
  for (let r = 1; r <= t.currentRound; r++) {
    hHTML += `<th style="padding:10px;">R${r}</th>`;
  }
  hHTML += '<th style="padding:10px;">总积分</th><th style="padding:10px;">对手分 (Buchholz)</th><th style="padding:10px;">初始ELO</th></tr>';
  sHead.innerHTML = hHTML;

  const sBody = document.getElementById('standingsBody');
  sBody.innerHTML = standings.map((p, idx) => {
    let rScoresHTML = '';
    for (let r = 0; r < t.currentRound; r++) {
      const sc = p.scores[r] !== undefined ? p.scores[r] : '-';
      let colorStyle = '';
      if (sc === 1) colorStyle = 'color:var(--green);font-weight:900;';
      else if (sc === 0) colorStyle = 'color:var(--red);font-weight:700;';
      else if (sc === 0.5) colorStyle = 'color:var(--yellow);font-weight:900;';
      rScoresHTML += `<td style="padding:10px;text-align:center;${colorStyle}">${sc}</td>`;
    }

    return `
      <tr style="border-bottom:1px solid var(--border);">
        <td style="padding:10px;text-align:center;font-weight:900;">${idx + 1}</td>
        <td style="padding:10px;text-align:left;font-weight:900;">${p.name}</td>
        ${rScoresHTML}
        <td style="padding:10px;text-align:center;font-weight:900;color:var(--pri);">${p.totalPoints.toFixed(1)}</td>
        <td style="padding:10px;text-align:center;font-weight:700;color:var(--text2);">${p.buchholz.toFixed(1)}</td>
        <td style="padding:10px;text-align:center;color:var(--text2);">${p.elo}</td>
      </tr>`;
  }).join('');
}

// --- K-Factor ELO Calculator ---
function calcKFactor(elo, totalGames) {
  if (totalGames < 20 || elo < 400) return 24;
  if (elo < 700) return 16;
  return 8;
}

function calcExpected(playerElo, opponentElo) {
  return 1 / (1 + Math.pow(10, (opponentElo - playerElo) / 400));
}

function calcEloChange(playerElo, opponentElo, actualScore, K) {
  const expected = calcExpected(playerElo, opponentElo);
  return Math.round(K * (actualScore - expected));
}

// --- End Tournament & Sync to Cloud ---
async function endTournament() {
  const t = currentTournament;
  if (!t) return;
  if (!confirm(`确定结束比赛「${t.name}」并将对局成绩与 ELO 结算结果同步到云端表格吗？`)) return;

  toast('⏳ 正在计算 ELO 并同步所有对局到云端...', 'info');

  const eloChanges = {};
  t.players.forEach(p => {
    eloChanges[p.id] = { name: p.name, oldElo: p.elo, delta: 0, games: 0 };
  });

  // Calculate ELO changes round by round
  for (let ri = 0; ri < t.rounds.length; ri++) {
    const roundObj = t.rounds[ri];
    for (const match of roundObj.pairings) {
      if (match.result === 'bye' || !match.blackId) continue;

      const redP = t.players.find(x => x.id === match.redId);
      const blackP = t.players.find(x => x.id === match.blackId);
      if (!redP || !blackP) continue;

      const curRedElo = redP.elo + (eloChanges[redP.id]?.delta || 0);
      const curBlackElo = blackP.elo + (eloChanges[blackP.id]?.delta || 0);

      const redK = calcKFactor(curRedElo, (eloChanges[redP.id]?.games || 0) + 10);
      const blackK = calcKFactor(curBlackElo, (eloChanges[blackP.id]?.games || 0) + 10);

      let redActual = 0.5, blackActual = 0.5;
      let resText = '🤝 和棋 (0.5 - 0.5)';
      let verdict = '双方战和';

      if (match.result === 'red') {
        redActual = 1; blackActual = 0;
        resText = '🔴 红胜 (1 - 0)';
        verdict = match.redName + ' 胜';
      } else if (match.result === 'black') {
        redActual = 0; blackActual = 1;
        resText = '⚫ 黑胜 (0 - 1)';
        verdict = match.blackName + ' 胜';
      }

      const redDelta = calcEloChange(curRedElo, curBlackElo, redActual, redK);
      const blackDelta = calcEloChange(curBlackElo, curRedElo, blackActual, blackK);

      eloChanges[redP.id].delta += redDelta;
      eloChanges[redP.id].games++;
      eloChanges[blackP.id].delta += blackDelta;
      eloChanges[blackP.id].games++;

      // POST to Google Sheets
      try {
        await fetch(GAS_API_URL, {
          method: 'POST',
          body: JSON.stringify({
            action: 'addMatch',
            pin: getAuthPin(),
            date: t.createdAt,
            round: `${t.name} R${ri + 1}`,
            redId: match.redId,
            redName: match.redName,
            result: resText,
            blackId: match.blackId,
            blackName: match.blackName,
            verdict,
            redEloDelta: redDelta,
            blackEloDelta: blackDelta,
            recordImage: null
          })
        });
      } catch (err) {
        console.error('Match sync error:', err);
      }
    }
  }

  // Summary
  let summary = `🏆 比赛「${t.name}」ELO 积分结算清单 (K=24/16/8体系):

`;
  Object.values(eloChanges).forEach(c => {
    const sign = c.delta >= 0 ? '+' : '';
    summary += `👤 ${c.name}: ${c.oldElo} → ${c.oldElo + c.delta} (${sign}${c.delta} 分)
`;
  });
  alert(summary);

  t.status = 'completed';
  saveTournaments();
  await loadAllData();
  toast('🎉 比赛圆满结束！对局记录与 ELO 积分已全自动同步完成。', 'success');
  renderTournamentManage();
}

// ============================================================
//  📋 SP98 BATCH IMPORTER (Parse raw Swiss Perfect text)
// ============================================================
function parseSP98Batch() {
  const text = document.getElementById('sp98Text').value.trim();
  const preview = document.getElementById('parsedPreview');
  const submitBtn = document.getElementById('btnSubmitSP98Batch');

  if (!text) {
    toast('请先粘贴 SP98 赛果文本！', 'error');
    return;
  }

  const lines = text.split('\n');
  parsedSP98Matches = [];

  lines.forEach(rawLine => {
    const line = rawLine.trim();
    if (!line) return;

    // Match scores: 1-0, 0-1, 0.5-0.5, 1/2-1/2, 和
    const resPattern = /(1\s*[-:]\s*0|0\s*[-:]\s*1|0\.5\s*[-:]\s*0\.5|1\/2\s*[-:]\s*1\/2|和)/i;
    const match = line.match(resPattern);

    if (match) {
      const parts = line.split(match[0]);
      let redRaw = parts[0].replace(/^[0-9\.\s]+/, '').replace(/\[.*?\]|\(.*?\)/g, '').trim();
      let blackRaw = parts[1].replace(/\[.*?\]|\(.*?\)/g, '').trim();

      // Find matching students in allStudents
      const redStudent = allStudents.find(s => s.cnName.trim() === redRaw || redRaw.includes(s.cnName.trim()));
      const blackStudent = allStudents.find(s => s.cnName.trim() === blackRaw || blackRaw.includes(s.cnName.trim()));

      let resType = 'draw';
      let resText = '🤝 和棋 (0.5 - 0.5)';
      if (match[0].replace(/\s+/g, '') === '1-0' || match[0].includes('1:0')) {
        resType = 'red';
        resText = '🔴 红胜 (1 - 0)';
      } else if (match[0].replace(/\s+/g, '') === '0-1' || match[0].includes('0:1')) {
        resType = 'black';
        resText = '⚫ 黑胜 (0 - 1)';
      }

      parsedSP98Matches.push({
        redName: redStudent ? redStudent.cnName : redRaw,
        redId: redStudent ? redStudent.id : '',
        redElo: redStudent ? redStudent.elo : 200,
        blackName: blackStudent ? blackStudent.cnName : blackRaw,
        blackId: blackStudent ? blackStudent.id : '',
        blackElo: blackStudent ? blackStudent.elo : 200,
        resType,
        resText,
        matched: !!(redStudent && blackStudent),
        raw: line
      });
    }
  });

  if (parsedSP98Matches.length === 0) {
    preview.style.display = 'block';
    preview.innerHTML = '<div style="color:var(--red);font-weight:700;">⚠️ 未能成功识别任何对局，请检查格式是否包含棋手与比分（如：林家豪 1 - 0 陈美仪）。</div>';
    if (submitBtn) submitBtn.style.display = 'none';
  } else {
    preview.style.display = 'block';
    const allMatched = parsedSP98Matches.every(m => m.matched);
    let html = `<div style="font-weight:900;color:var(--pri);margin-bottom:10px;">✅ 成功识别 ${parsedSP98Matches.length} 盘 SP98 对局：</div>`;
    html += parsedSP98Matches.map((m, i) => `
      <div style="background:#fff;border:1px solid var(--border);border-radius:8px;padding:8px 12px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;font-size:13px;">
        <div>
          <span style="font-weight:800;color:var(--pri);">#${i + 1}</span>
          <span style="margin-left:8px;font-weight:700;">${m.redName}</span>
          ${m.redId ? `<span style="font-size:11px;color:var(--text2);">(${m.redId})</span>` : '<span style="color:red;font-size:11px;">[未建档]</span>'}
          <span style="color:var(--text2);margin:0 6px;">VS</span>
          <span style="font-weight:700;">${m.blackName}</span>
          ${m.blackId ? `<span style="font-size:11px;color:var(--text2);">(${m.blackId})</span>` : '<span style="color:red;font-size:11px;">[未建档]</span>'}
        </div>
        <div style="font-weight:800;">${m.resText}</div>
      </div>
    `).join('');

    if (!allMatched) {
      html += '<div style="margin-top:10px;font-size:12px;color:var(--red);font-weight:700;">⚠️ 提示：部分棋手姓名未能匹配到系统档案，请先在「学员快速建档」登记后再导入。</div>';
    }

    preview.innerHTML = html;
    if (submitBtn) submitBtn.style.display = 'block';
  }
}

async function submitSP98Batch() {
  if (!parsedSP98Matches.length) {
    parseSP98Batch();
  }
  if (!parsedSP98Matches.length) return;

  const tourneyName = document.getElementById('sp98BatchTourneyName').value.trim() || 'SP98 赛事';
  if (!confirm(`确定将识别出的 ${parsedSP98Matches.length} 盘对局提交入库并同步更新 ELO 积分吗？`)) return;

  toast(`⏳ 正在同步录入 ${parsedSP98Matches.length} 盘对局...`, 'info');

  const today = new Date().toISOString().split('T')[0];
  let successCount = 0;

  for (let i = 0; i < parsedSP98Matches.length; i++) {
    const m = parsedSP98Matches[i];
    let verdict = '双方战和';
    let redActual = 0.5, blackActual = 0.5;

    if (m.resType === 'red') {
      verdict = m.redName + ' 胜';
      redActual = 1; blackActual = 0;
    } else if (m.resType === 'black') {
      verdict = m.blackName + ' 胜';
      redActual = 0; blackActual = 1;
    }

    const redK = calcKFactor(m.redElo, 10);
    const blackK = calcKFactor(m.blackElo, 10);
    const redDelta = calcEloChange(m.redElo, m.blackElo, redActual, redK);
    const blackDelta = calcEloChange(m.blackElo, m.redElo, blackActual, blackK);

    try {
      await fetch(GAS_API_URL, {
        method: 'POST',
        body: JSON.stringify({
          action: 'addMatch',
          pin: getAuthPin(),
          date: today,
          round: `${tourneyName} #${i + 1}`,
          redId: m.redId,
          redName: m.redName,
          result: m.resText,
          blackId: m.blackId,
          blackName: m.blackName,
          verdict,
          redEloDelta: redDelta,
          blackEloDelta: blackDelta,
          recordImage: null
        })
      });
      successCount++;
    } catch (e) {
      console.error(e);
    }
  }

  document.getElementById('sp98Text').value = '';
  document.getElementById('parsedPreview').style.display = 'none';
  document.getElementById('btnSubmitSP98Batch').style.display = 'none';
  parsedSP98Matches = [];

  await loadAllData();
  toast(`🎉 成功批量录入 ${successCount} 盘对局，天梯榜与学员 ELO 已实时更新！`, 'success');
}

// Auto-render tournament list when switching to tab
const origSwitchTab = switchTab;
switchTab = function(t) {
  origSwitchTab(t);
  if (t === 'tournament') {
    showTournamentList();
  }
};


// ── DELETION & CLEANUP FUNCTIONS ──────────────────────────────
async function deleteSingleMatch(date, round, redName, blackName) {
  if (!confirm(`确定删除对局记录：${date} ${round} (${redName} vs ${blackName}) 吗？`)) return;
  toast('⏳ 正在从云端删除对局记录...', 'info');
  try {
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'deleteMatch', date, round, redName, blackName, pin: getAuthPin() })
    });
    const d = await res.json();
    if (d.success || d.status === 'ok') {
      toast('✅ 对局记录已成功删除！', 'success');
      await loadMatches();
      renderGallery();
    } else {
      toast('删除失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

async function clearAllTestMatches() {
  const code = prompt('⚠️ 警告：此操作将清空「实战对局记录表」中的全部对局历史数据！\n\n如确认清空，请输入总控密码:');
  if (code !== getAuthPin()) {
    if (code !== null) toast('密码错误，操作取消。', 'warning');
    return;
  }
  toast('⏳ 正在清空云端所有历史对局...', 'info');
  try {
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'clearTestData', pin: getAuthPin() })
    });
    const d = await res.json();
    if (d.success || d.status === 'ok') {
      toast('🎉 所有实战对局记录已清空！', 'success');
      await loadMatches();
      renderGallery();
    } else {
      toast('清空失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

async function deleteStudentAccount(studentId, studentName) {
  if (!confirm(`⚠️ 危险操作：确定要彻底删除学员「${studentName}」(${studentId}) 吗？\n\n删除后，该学员将从「学员档案总册」和「天梯榜」完全注销移除！`)) return;
  toast(`⏳ 正在注销学员 ${studentName}...`, 'info');
  try {
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'deleteStudent', studentId, pin: getAuthPin() })
    });
    const d = await res.json();
    if (d.success || d.status === 'ok') {
      toast(`✅ 学员 ${studentName} (${studentId}) 已成功删除移除！`, 'success');
      await loadAllData();
    } else {
      toast('删除失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}


// ── CLOUDFLARE WORKER LICENSE MANAGEMENT ──────────────────────
const CF_WORKER_URL = 'https://cxb-license.clubxiangqibera.workers.dev';
let lastGeneratedKey = '';

async function createSchoolLicense() {
  const schoolName = document.getElementById('licSchoolName').value.trim();
  const validDays = document.getElementById('licValidDays').value;
  const maxRounds = document.getElementById('licMaxRounds').value;

  if (!schoolName) {
    toast('请输入租用学校名称！', 'error');
    return;
  }

  toast('⏳ 正在向 Cloudflare Worker 写入授权...', 'info');

  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/create-license`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        adminPin: getAuthPin(),
        schoolName,
        validDays,
        maxRounds
      })
    });
    const d = await res.json();

    if (d.success) {
      lastGeneratedKey = d.licenseKey;
      document.getElementById('generatedLicBox').style.display = 'block';
      document.getElementById('displayGeneratedKey').textContent = d.licenseKey;
      toast(`✅ 成功为「${schoolName}」生成授权激活码！`, 'success');
      loadSchoolLicenses();
    } else {
      toast('生成失败: ' + (d.error || ''), 'error');
    }
  } catch (e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

function copyGeneratedLicense() {
  const schoolName = document.getElementById('licSchoolName').value.trim() || '学校比赛';
  const textToCopy = `【百乐象棋俱乐部 · 赛事系统授权激活码】\n学校/赛事: ${schoolName}\n比赛登录网址: https://clubxiangqibera.github.io/school.html\n激活码: ${lastGeneratedKey}\n\n* 请在有效租期内使用，预祝比赛圆满举行！`;
  navigator.clipboard.writeText(textToCopy);
  toast('✅ 激活码已复制，可直接粘贴发到 WhatsApp！', 'success');
}

async function loadSchoolLicenses() {
  const container = document.getElementById('licensesTableContainer');
  container.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text2);">⏳ 正在从 Cloudflare KV 读取数据...</div>';

  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/list-licenses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin() })
    });
    const d = await res.json();

    if (d.success && d.list) {
      if (!d.list.length) {
        container.innerHTML = '<div style="padding:30px;text-align:center;color:var(--text2);">暂无在约授权码。在上方输入学校即可一键生成！</div>';
        return;
      }

      container.innerHTML = `
        <table style="width:100%; border-collapse:collapse; font-size:13px;">
          <thead>
            <tr style="background:var(--bg); border-bottom:2px solid var(--border);">
              <th style="padding:10px 12px; text-align:left;">授权激活码</th>
              <th style="padding:10px 12px; text-align:left;">授权学校 / 赛事</th>
              <th style="padding:10px 12px; text-align:center;">状态</th>
              <th style="padding:10px 12px; text-align:left;">到期时间 (本地时间)</th>
              <th style="padding:10px 12px; text-align:center;">操作</th>
            </tr>
          </thead>
          <tbody>
            ${d.list.map(item => `
              <tr style="border-bottom:1px solid var(--border);">
                <td style="padding:10px 12px; font-weight:900; color:var(--pri); font-family:monospace; font-size:14px;">${item.key}</td>
                <td style="padding:10px 12px; font-weight:800;">${item.school}</td>
                <td style="padding:10px 12px; text-align:center;">
                  ${item.status === 'ended' 
                    ? '<span class="badge" style="background:#EAECEE;color:#7F8C8D;font-size:11px;">⛔ 已终止停用</span>'
                    : (new Date(item.expiresAt).getTime() < Date.now() 
                        ? '<span class="badge" style="background:#FDEDEC;color:#C0392B;font-size:11px;">⏰ 租约已超期</span>' 
                        : '<span class="badge badge-green" style="font-size:11px;">🟢 租期有效</span>')}
                </td>
                <td style="padding:10px 12px; font-size:12px; color:var(--text2);">
                  ${item.expiresAt ? new Date(item.expiresAt).toLocaleString('zh-CN', {month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hour12:false}) : '-'}
                </td>
                <td style="padding:10px 12px; text-align:center;">
                  <div style="display:inline-flex; gap:6px; flex-wrap:wrap; justify-content:center; align-items:center;">
                    <button class="btn-sm green" style="padding:4px 8px; font-size:11px;" onclick="extendSchoolLicense('${item.key}', 1)" title="顺延比赛时间 1 天">
                      ⏳ +1天
                    </button>
                    <button class="btn-sm green" style="padding:4px 8px; font-size:11px;" onclick="extendSchoolLicense('${item.key}', 3)" title="顺延比赛时间 3 天">
                      ⏳ +3天
                    </button>
                    ${item.status === 'ended' ? `
                      <button class="btn-sm" style="color:var(--pri2); border-color:var(--pri2); padding:4px 8px; font-size:11px;" onclick="resumeSchoolLicense('${item.key}')" title="重新激活该授权">
                        ▶️ 重新启用
                      </button>
                    ` : `
                      <button class="btn-sm" style="color:var(--red); border-color:var(--red); padding:4px 8px; font-size:11px;" onclick="endSchoolLicense('${item.key}')" title="终止开赛权限（保留记录）">
                        ⛔ 终止开赛
                      </button>
                    `}
                    <button class="btn-sm" style="color:#7F8C8D; border-color:#BDC3C7; padding:4px 8px; font-size:11px;" onclick="revokeSchoolLicense('${item.key}')" title="彻底删除此授权码记录">
                      🗑️ 彻底移除
                    </button>
                  </div>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>`;
    } else {
      container.innerHTML = `<div style="padding:20px;text-align:center;color:var(--red);">读取失败: ${d.error || ''}</div>`;
    }
  } catch (e) {
    container.innerHTML = `<div style="padding:20px;text-align:center;color:var(--red);">网络错误: ${e.message}</div>`;
  }
}


async function extendSchoolLicense(key, days) {
  toast(`⏳ 正在为授权码 ${key} 延长 ${days} 天租期...`, 'info');
  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/extend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), licenseKey: key, addDays: days })
    });
    const d = await res.json();
    if (d.success) {
      toast(`🎉 ${d.message}`, 'success');
      loadSchoolLicenses();
    } else {
      toast('续期失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

async function endSchoolLicense(key) {
  if (!confirm(`确定提前终止授权码「${key}」吗？\n\n终止后，学校端将无法再开赛或登录，但该记录依然保留在列表以供日后查阅或重新启用！`)) return;
  toast('⏳ 正在终止授权...', 'info');
  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/end-key`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), licenseKey: key })
    });
    const d = await res.json();
    if (d.success) {
      toast(`⛔ ${d.message}`, 'success');
      loadSchoolLicenses();
    } else {
      toast('终止失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

async function resumeSchoolLicense(key) {
  toast('⏳ 正在重新激活授权...', 'info');
  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/resume-key`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), licenseKey: key })
    });
    const d = await res.json();
    if (d.success) {
      toast(`✅ ${d.message}`, 'success');
      loadSchoolLicenses();
    } else {
      toast('恢复失败: ' + (d.error || ''), 'error');
    }
  } catch(e) {
    toast('网络错误: ' + e.message, 'error');
  }
}

async function revokeSchoolLicense(key) {
  if (!confirm(`确定彻底注销并吊销授权码「${key}」吗？学校将立即无法继续开赛！`)) return;
  toast('⏳ 正在从 Cloudflare KV 删除授权...', 'info');

  try {
    const res = await fetch(`${CF_WORKER_URL}/api/admin/revoke`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), licenseKey: key })
    });
    const d = await res.json();
    if (d.success) {
      toast(`✅ 授权码 ${key} 已成功吊销！`, 'success');
      loadSchoolLicenses();
    } else {
      toast('吊销失败: ' + (d.error || ''), 'error');
    }
  } catch (e) {
    toast('网络错误: ' + e.message, 'error');
  }
}


// --- Coach Management JS ---
async function loadCoaches() {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/coaches?adminPin=' + getAuthPin());
    const data = await res.json();
    if (data.success) {
      window._coaches = data.coaches || [];
      renderCoaches();
    }
  } catch (e) {
    console.error("Failed to load coaches");
  }
}

function renderCoaches() {
  const container = document.getElementById('coachListTable');
  if (!container) return;
  
  if (window._coaches.length === 0) {
    container.innerHTML = '<div style="padding:10px;color:var(--text2);">暂无教练账号。</div>';
    return;
  }

  let html = `<table class="cxb-table" style="width:100%; border-collapse: collapse;">
    <thead><tr style="border-bottom:2px solid var(--border); text-align:left;">
      <th style="padding:10px;">姓名</th>
      <th style="padding:10px;">PIN</th>
      <th style="padding:10px;">权限配置</th>
      <th style="padding:10px; text-align:right;">操作</th>
    </tr></thead><tbody>`;

  const availablePerms = [
    {id: 'dashboard', name: '运营看板'},
    {id: 'matches', name: '对局档案'},
    {id: 'tournament', name: '锦标赛'},
    {id: 'ladder', name: '天梯榜'},
    {id: 'students', name: '学员建档'},
    {id: 'payments', name: '学费审核'},
    {id: 'licenses', name: '授权管理'}
  ];

  window._coaches.forEach((c, i) => {
    let permsHtml = availablePerms.map(p => {
      const checked = (c.perms && c.perms.includes(p.id)) ? 'checked' : '';
      return `<label style="margin-right:8px;font-size:12px;cursor:pointer;"><input type="checkbox" onchange="toggleCoachPerm(${i}, '${p.id}')" ${checked}> ${p.name}</label>`;
    }).join('');

    html += `<tr style="border-bottom:1px solid var(--border);">
      <td style="padding:10px;"><b>${c.name}</b></td>
      <td style="padding:10px;color:var(--text2);">${c.pin}</td>
      <td style="padding:10px;"><div style="display:flex;flex-wrap:wrap;gap:4px;">${permsHtml}</div></td>
      <td style="padding:10px; text-align:right;">
        <button onclick="deleteCoach(${i})" class="btn" style="background:var(--red);color:#fff;padding:6px 12px;border:none;border-radius:8px;cursor:pointer;">删除</button>
      </td>
    </tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

async function saveCoaches(coaches) {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/coaches', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), coaches: coaches })
    });
    const data = await res.json();
    if (data.success) {
      if(typeof toast === 'function') toast('教练列表已保存', 'success');
      window._coaches = coaches;
      renderCoaches();
    } else {
      if(typeof toast === 'function') toast('保存失败', 'error');
    }
  } catch(e) {
    if(typeof toast === 'function') toast('网络错误', 'error');
  }
}

async function addCoach() {
  const name = document.getElementById('newCoachName').value.trim();
  const pin = document.getElementById('newCoachPin').value.trim();
  if (!name || !pin) {
    if(typeof toast === 'function') toast('请填写姓名和PIN', 'error');
    return;
  }
  const coaches = [...(window._coaches || [])];
  coaches.push({
    id: 'coach_' + Date.now(),
    name: name,
    pin: pin,
    perms: ['dashboard', 'matches', 'tournament', 'ladder', 'students', 'payments', 'licenses']
  });
  await saveCoaches(coaches);
  document.getElementById('newCoachName').value = '';
  document.getElementById('newCoachPin').value = '';
}

async function deleteCoach(idx) {
  if (!confirm("确定要删除该教练吗？")) return;
  const coaches = [...(window._coaches || [])];
  coaches.splice(idx, 1);
  await saveCoaches(coaches);
}

async function toggleCoachPerm(idx, permId) {
  const coaches = [...(window._coaches || [])];
  const c = coaches[idx];
  if (!c.perms) c.perms = [];
  if (c.perms.includes(permId)) {
    c.perms = c.perms.filter(p => p !== permId);
  } else {
    c.perms.push(permId);
  }
  await saveCoaches(coaches);
}

// Hook into loadAllData or init to call loadCoaches if superadmin
if (typeof loadAllData !== 'undefined') {
  const originalLoadAllData = loadAllData;
  loadAllData = function() {
    originalLoadAllData();
    const user = JSON.parse(localStorage.getItem('cxb_auth_user'));
    if (user && user.role === 'superadmin') {
      loadCoaches();
    }
  };
}
// --- End Coach Management JS ---


// --- Gallery Upload & Management JS ---
async function loadEvents() {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/events');
    const data = await res.json();
    window._events = data.events || data || [];
    renderEvents();
  } catch(e) { console.error('Failed to load events'); }
}

function renderEvents() {
  const container = document.getElementById('galleryListArea');
  if(!container) return;
  if(!window._events || window._events.length === 0) {
    container.innerHTML = '<div style="color:var(--text2);">暂无活动相册，点击上方新建。</div>';
    return;
  }
  let html = '';
  window._events.forEach((evt, idx) => {
    const coverId = evt.photos && evt.photos.length > 0 ? evt.photos[0] : '';
    const coverUrl = coverId ? 'https://drive.google.com/thumbnail?sz=w800&id=' + coverId : '';
    html += `<div style="background:var(--bg); border-radius:12px; overflow:hidden; border:1px solid var(--border);">
      <div style="height:160px; background:#ddd url('${coverUrl}') center/cover;"></div>
      <div style="padding:16px;">
        <div style="font-weight:900; font-size:15px; margin-bottom:4px;">${evt.name}</div>
        <div style="font-size:12px; color:var(--text2); margin-bottom:12px;">📅 ${evt.date} · 📸 ${evt.photos ? evt.photos.length : 0} 张照片</div>
        <div style="display:flex; gap:8px;">
          <button onclick="editEvent(${idx})" class="btn" style="flex:1; padding:6px; background:#E8F8F5; color:#1ABC9C; border:none; border-radius:8px; font-weight:700;">编辑</button>
          <button onclick="deleteEvent(${idx})" class="btn" style="flex:1; padding:6px; background:#FDEDEC; color:#E74C3C; border:none; border-radius:8px; font-weight:700;">删除</button>
        </div>
      </div>
    </div>`;
  });
  container.innerHTML = html;
}

async function submitGallery() {
  const name = document.getElementById('galName').value.trim();
  const date = document.getElementById('galDate').value;
  const desc = document.getElementById('galDesc').value.trim();
  const fileInput = document.getElementById('galFiles');
  if(!name || !date || fileInput.files.length === 0) {
    if(typeof toast === 'function') toast('请填写完整名称、日期，并至少选择一张照片', 'error');
    return;
  }

  const btn = document.getElementById('galSubmitBtn');
  const prog = document.getElementById('galUploadProgress');
  btn.disabled = true;
  btn.textContent = '压缩并上传中...';
  prog.style.display = 'block';

  let uploadedIds = [];
  const files = fileInput.files;
  for(let i=0; i<files.length; i++) {
    prog.textContent = `正在处理并上传 第 ${i+1} / ${files.length} 张...`;
    try {
      const base64 = await compressImage(files[i]);
      const res = await fetch(GAS_API_URL, {
        method: 'POST',
        body: JSON.stringify({ action: 'uploadEventPhoto', eventName: name, imageBase64: base64 })
      });
      const data = await res.json();
      if(data.error && data.error.includes('未知操作')) {
        alert('上传失败！系统检测到你的 Google Apps Script 还没更新发布。请按照我说的方法，去更新并部署新版 Code.gs！');
        break; // stop uploading
      }
      if(data.success && data.fileId) {
        uploadedIds.push(data.fileId);
      } else {
        console.error('GAS Error:', data.error);
        if(typeof toast === 'function') toast('上传第'+(i+1)+'张失败: ' + (data.error||''), 'error');
      }
    } catch(e) {
      console.error('Upload failed for file', i);
    }
  }

  prog.textContent = '照片上传完成，正在保存图集数据...';
  
  const newEvent = { id: 'evt_'+Date.now(), name, date, desc, photos: uploadedIds };
  const events = [...(window._events || []), newEvent];
  
  try {
    const res2 = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), events: events })
    });
    const data2 = await res2.json();
    if(data2.success) {
      if(typeof toast === 'function') toast('相册创建成功！', 'success');
      document.getElementById('createGalleryModal').style.display = 'none';
      window._events = events;
      renderEvents();
      // clear form
      document.getElementById('galName').value = '';
      document.getElementById('galDate').value = '';
      document.getElementById('galDesc').value = '';
      fileInput.value = '';
    } else {
      if(typeof toast === 'function') toast('保存失败', 'error');
    }
  } catch(e) {
    if(typeof toast === 'function') toast('网络错误', 'error');
  }

  btn.disabled = false;
  btn.textContent = '开始上传';
  prog.style.display = 'none';
}

async function deleteEvent(idx) {
  if(!confirm('确定删除这个图集吗？照片将留在云端，但网页将不再展示。')) return;
  const events = [...(window._events || [])];
  events.splice(idx, 1);
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), events: events })
    });
    const result = await res.json();
    if(result.success) {
      if(typeof toast === 'function') toast('已删除', 'success');
      window._events = events;
      renderEvents();
    }
  } catch(e) {}
}



async function editEvent(idx) {
  const evt = window._events[idx];
  document.getElementById('editGalIdx').value = idx;
  document.getElementById('editGalName').value = evt.name;
  document.getElementById('editGalDate').value = evt.date;
  document.getElementById('editGalDesc').value = evt.desc || '';
  
  // Render existing photos
  const photoContainer = document.getElementById('editGalPhotos');
  photoContainer.innerHTML = '';
  if (evt.photos && evt.photos.length) {
    evt.photos.forEach((pid, pidx) => {
      photoContainer.innerHTML += `<div style="position:relative; width:60px; height:60px; border-radius:8px; overflow:hidden; border:1px solid #ddd; background:url('https://drive.google.com/thumbnail?sz=w100&id=${pid}') center/cover;">
        <div onclick="removePhotoFromEdit(${idx}, ${pidx})" style="position:absolute; top:0; right:0; background:rgba(231,76,60,0.9); color:#fff; width:20px; height:20px; text-align:center; line-height:20px; font-size:12px; cursor:pointer; font-weight:bold;">&times;</div>
      </div>`;
    });
  }
  
  document.getElementById('editGalleryModal').style.display = 'flex';
}

function removePhotoFromEdit(evtIdx, photoIdx) {
  if(!confirm('确定移除这张照片吗？')) return;
  window._events[evtIdx].photos.splice(photoIdx, 1);
  editEvent(evtIdx); // re-render modal
}

async function submitEditGallery() {
  const idx = document.getElementById('editGalIdx').value;
  const evt = window._events[idx];
  
  const name = document.getElementById('editGalName').value.trim();
  const date = document.getElementById('editGalDate').value;
  const desc = document.getElementById('editGalDesc').value.trim();
  const fileInput = document.getElementById('editGalFiles');
  
  if(!name || !date) {
    toast('名称和日期必填', 'error'); return;
  }
  
  const btn = document.getElementById('editGalSubmitBtn');
  const prog = document.getElementById('editGalProgress');
  btn.disabled = true;
  btn.textContent = '保存中...';
  
  let newUploadedIds = [];
  const files = fileInput.files;
  if (files.length > 0) {
    prog.style.display = 'block';
    for(let i=0; i<files.length; i++) {
      prog.textContent = `上传新照片 ${i+1}/${files.length}...`;
      try {
        const base64 = await compressImage(files[i]);
        const res = await fetch(GAS_API_URL, {
          method: 'POST',
          body: JSON.stringify({ action: 'uploadEventPhoto', eventName: name, imageBase64: base64 })
        });
        const data = await res.json();
        if(data.success && data.fileId) newUploadedIds.push(data.fileId);
      } catch(e){}
    }
  }
  
  prog.textContent = '保存数据...';
  
  evt.name = name;
  evt.date = date;
  evt.desc = desc;
  if(!evt.photos) evt.photos = [];
  evt.photos = evt.photos.concat(newUploadedIds);
  
  try {
    const res2 = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ adminPin: getAuthPin(), events: window._events })
    });
    const data2 = await res2.json();
    if(data2.success) {
      toast('修改成功！', 'success');
      document.getElementById('editGalleryModal').style.display = 'none';
      renderEvents();
      fileInput.value = '';
    } else {
      toast('保存失败', 'error');
    }
  } catch(e) {
    toast('网络错误', 'error');
  }

  btn.disabled = false;
  btn.textContent = '保存修改';
  prog.style.display = 'none';
}
'''

# Replace old editEvent
old_js_edit = re.search(r'async function editEvent\(idx\) \{.*?\n\}', text, re.DOTALL)
if old_js_edit:
    text = text.replace(old_js_edit.group(0), js_edit)
else:
    text = text.replace('

function compressImage(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        let w = img.width; let h = img.height;
        const max = 1200;
        if(w > max || h > max) {
          if(w > h) { h = h * (max / w); w = max; }
          else { w = w * (max / h); h = max; }
        }
        canvas.width = w; canvas.height = h;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, w, h);
        resolve(canvas.toDataURL('image/jpeg', 0.8));
      };
    };
  });
}

// Hook into loadAllData or showApp to load events
if(typeof loadAllData !== 'undefined') {
  const oldLoadAllData = loadAllData;
  loadAllData = function() {
    oldLoadAllData();
    const user = JSON.parse(localStorage.getItem('cxb_auth_user'));
    if (user && user.role === 'superadmin') {
       loadEvents();
    }
  };
}
// --- End Gallery JS ---
