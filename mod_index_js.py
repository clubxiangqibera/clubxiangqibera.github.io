import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

html_block = '''
      <!-- 5. EVENTS GALLERY -->
      <div class="section-head" style="margin-top:40px;">
        <div class="section-title">📸 历届活动相册</div>
        <div class="section-sub">记录在百乐县中国象棋公会的精彩瞬间</div>
      </div>
      <div id="publicGalleryArea" style="display:grid; gap:16px; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); margin-top:16px; margin-bottom:40px;">
        <div style="color:var(--text2); font-size:13px; padding:10px;">正在加载相册...</div>
      </div>

      <!-- PHOTO MODAL -->
      <div id="photoModal" class="modal-overlay" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.9); z-index:9999; flex-direction:column; align-items:center; justify-content:center; padding:20px;">
        <button onclick="document.getElementById('photoModal').style.display='none'" style="position:absolute; top:20px; right:20px; background:none; border:none; color:#fff; font-size:32px; cursor:pointer; z-index:10000;">&times;</button>
        <div id="photoModalContent" style="width:100%; max-width:800px; height:80vh; overflow-y:auto; display:flex; flex-direction:column; gap:16px; align-items:center;">
        </div>
      </div>
'''
text = text.replace('<!-- 4. LEADERBOARD / PODIUM -->', html_block + '\n      <!-- 4. LEADERBOARD / PODIUM -->')

js_block = '''
// --- Public Gallery JS ---
async function loadPublicEvents() {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/events');
    const events = await res.json();
    const container = document.getElementById('publicGalleryArea');
    if(!events || events.length === 0) {
      container.innerHTML = '<div style="color:var(--text2); font-size:13px;">暂无公开相册。</div>';
      return;
    }
    let html = '';
    events.forEach((evt, idx) => {
      const coverId = evt.photos && evt.photos.length > 0 ? evt.photos[0] : '';
      const coverUrl = coverId ? 'https://drive.google.com/uc?export=view&id=' + coverId : '';
      html += `<div style="background:var(--card); border-radius:16px; overflow:hidden; box-shadow:var(--shadow); cursor:pointer; transition:transform 0.2s;" onclick="openEventPhotos(${idx})" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
        <div style="height:180px; background:#ddd url('${coverUrl}') center/cover;"></div>
        <div style="padding:16px;">
          <div style="font-weight:900; font-size:16px; color:var(--text); margin-bottom:6px;">${evt.name}</div>
          <div style="font-size:12px; color:var(--text2); margin-bottom:8px;">📅 ${evt.date} · 📸 ${evt.photos ? evt.photos.length : 0} 张照片</div>
          <div style="font-size:13px; color:var(--text2); line-height:1.4;">${evt.desc || ''}</div>
        </div>
      </div>`;
    });
    container.innerHTML = html;
    window._publicEvents = events;
  } catch(e) {
    document.getElementById('publicGalleryArea').innerHTML = '<div style="color:var(--text2); font-size:13px;">相册加载失败。</div>';
  }
}

function openEventPhotos(idx) {
  const evt = window._publicEvents[idx];
  if(!evt || !evt.photos) return;
  const container = document.getElementById('photoModalContent');
  container.innerHTML = `<div style="color:#fff; font-size:20px; font-weight:900; margin-bottom:10px;">${evt.name}</div>`;
  evt.photos.forEach(id => {
    container.innerHTML += `<img src="https://drive.google.com/uc?export=view&id=${id}" style="width:100%; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.5); margin-bottom:16px;" loading="lazy">`;
  });
  document.getElementById('photoModal').style.display = 'flex';
}

// Hook into init
document.addEventListener('DOMContentLoaded', () => {
  loadPublicEvents();
});
// --- End Public Gallery JS ---
</script>
'''

text = text.replace('</script>', js_block)
with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Index HTML injected")
