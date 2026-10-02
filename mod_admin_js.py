import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

js_code = '''
// --- Gallery Upload & Management JS ---
async function loadEvents() {
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/events');
    const data = await res.json();
    window._events = data || [];
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
    const coverUrl = coverId ? 'https://drive.google.com/uc?export=view&id=' + coverId : '';
    html += `<div style="background:var(--bg); border-radius:12px; overflow:hidden; border:1px solid var(--border);">
      <div style="height:160px; background:#ddd url('${coverUrl}') center/cover;"></div>
      <div style="padding:16px;">
        <div style="font-weight:900; font-size:15px; margin-bottom:4px;">${evt.name}</div>
        <div style="font-size:12px; color:var(--text2); margin-bottom:12px;">📅 ${evt.date} · 📸 ${evt.photos ? evt.photos.length : 0} 张照片</div>
        <button onclick="deleteEvent(${idx})" class="btn" style="width:100%; padding:6px; background:#FDEDEC; color:#E74C3C; border:none; border-radius:8px; font-weight:700;">删除图集</button>
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
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ action: 'uploadEventPhoto', eventName: name, imageBase64: base64 })
      });
      const data = await res.json();
      if(data.success && data.fileId) {
        uploadedIds.push(data.fileId);
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
</script>
'''

text = text.replace('</script>', js_code)
with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("JS injected")
