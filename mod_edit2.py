import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

modal_html = '''
    <!-- EDIT GALLERY MODAL -->
    <div id="editGalleryModal" class="modal-overlay" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:999; align-items:center; justify-content:center;">
      <div style="background:#fff; width:90%; max-width:500px; border-radius:16px; padding:24px; max-height:90vh; overflow-y:auto;">
        <h3 style="margin-top:0; color:var(--pri);">编辑活动相册</h3>
        <input type="hidden" id="editGalIdx">
        <input type="text" id="editGalName" class="form-input" style="margin-bottom:12px;">
        <input type="date" id="editGalDate" class="form-input" style="margin-bottom:12px;">
        <textarea id="editGalDesc" class="form-input" style="margin-bottom:12px; height:80px; resize:vertical;"></textarea>
        
        <div style="margin-bottom:16px;">
          <div style="font-weight:700; font-size:13px; color:var(--text2); margin-bottom:8px;">已有照片 (点击删除)</div>
          <div id="editGalPhotos" style="display:flex; flex-wrap:wrap; gap:8px;"></div>
        </div>
        
        <div style="margin-bottom:16px; background:#F8F9F9; padding:12px; border-radius:10px; border:1px dashed #BDC3C7;">
          <label style="font-weight:700; font-size:13px; color:var(--text2); display:block; margin-bottom:8px;">添加新照片</label>
          <input type="file" id="editGalFiles" multiple accept="image/*" style="width:100%;">
        </div>
        <div id="editGalProgress" style="font-size:13px; color:var(--pri); font-weight:800; margin-bottom:16px; display:none;">正在上传...</div>
        
        <div style="display:flex; gap:10px; justify-content:flex-end;">
          <button class="btn" style="background:#BDC3C7; color:#fff; border:none; padding:8px 16px; border-radius:10px;" onclick="document.getElementById('editGalleryModal').style.display='none'">取消</button>
          <button id="editGalSubmitBtn" class="btn" style="background:var(--green); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800;" onclick="submitEditGallery()">保存修改</button>
        </div>
      </div>
    </div>
'''

if 'id="editGalleryModal"' not in text:
    text = text.replace('<!-- CREATE GALLERY MODAL -->', modal_html + '\n    <!-- CREATE GALLERY MODAL -->')

js_edit = '''
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
    text = text.replace('function compressImage', js_edit + '\nfunction compressImage')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Proper modal injected!")
