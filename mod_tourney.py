import io
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_pairing = '<div class="result-btn-group" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">'

new_pairing = '''<div class="result-btn-group" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
          <div style="grid-column:1/-1;text-align:center;font-size:12px;margin-bottom:4px;">
             <label style="cursor:pointer;color:var(--pri2);text-decoration:underline;">
                📎 附加对局记谱纸/照片
                <input type="file" style="display:none;" accept="image/*" onchange="uploadTourneyImg(${currentViewingRound}, ${bIdx}, this)">
             </label>
             <span id="t_img_status_${currentViewingRound}_${bIdx}" style="margin-left:8px;color:#27AE60;font-weight:bold;">
               ${p.recordImage ? '✅ 已附图' : ''}
             </span>
          </div>'''

text = text.replace(old_pairing, new_pairing)

script_add = '''
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
'''
text = text.replace('function renderTournamentManage() {', script_add + '\nfunction renderTournamentManage() {')

payload_old = "recordImage: ''"
payload_new = "recordImage: match.recordImage || ''"
text = text.replace(payload_old, payload_new)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
