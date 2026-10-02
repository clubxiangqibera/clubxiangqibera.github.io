import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

panel_html = '''
    <!-- GALLERY TAB -->
    <div class="tab-panel" id="panel-gallery">
      <div class="form-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div style="font-size:18px; font-weight:900;">📸 历届活动相册管理</div>
          <button class="btn" style="background:var(--green); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800; cursor:pointer;" onclick="document.getElementById('createGalleryModal').style.display='flex'">+ 创建新图集</button>
        </div>
        <div id="galleryListArea" style="display:grid; gap:16px; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));"></div>
      </div>
    </div>

    <!-- CREATE GALLERY MODAL -->
    <div id="createGalleryModal" class="modal-overlay" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:999; align-items:center; justify-content:center;">
      <div style="background:#fff; width:90%; max-width:500px; border-radius:16px; padding:24px; max-height:90vh; overflow-y:auto;">
        <h3 style="margin-top:0; color:var(--pri);">上传新活动相册</h3>
        <input type="text" id="galName" class="form-input" placeholder="活动名称 (例: 2026第一届棋缘教育营)" style="margin-bottom:12px;">
        <input type="date" id="galDate" class="form-input" style="margin-bottom:12px;">
        <textarea id="galDesc" class="form-input" placeholder="活动简短描述..." style="margin-bottom:12px; height:80px; resize:vertical;"></textarea>
        <div style="margin-bottom:16px; background:#F8F9F9; padding:12px; border-radius:10px; border:1px dashed #BDC3C7;">
          <label style="font-weight:700; font-size:13px; color:var(--text2); display:block; margin-bottom:8px;">选择多张照片上传 (自动压缩)</label>
          <input type="file" id="galFiles" multiple accept="image/*" style="width:100%;">
        </div>
        <div id="galUploadProgress" style="font-size:13px; color:var(--pri); font-weight:800; margin-bottom:16px; display:none;">正在上传 0 / 0 ...</div>
        <div style="display:flex; gap:10px; justify-content:flex-end;">
          <button class="btn" style="background:#BDC3C7; color:#fff; border:none; padding:8px 16px; border-radius:10px;" onclick="document.getElementById('createGalleryModal').style.display='none'">取消</button>
          <button id="galSubmitBtn" class="btn" style="background:var(--pri); color:#fff; border:none; padding:8px 16px; border-radius:10px; font-weight:800;" onclick="submitGallery()">开始上传</button>
        </div>
      </div>
    </div>
'''

if 'id="panel-gallery"' not in text:
    text = text.replace('<div class="modal-overlay" id="createTournamentModal">', panel_html + '\n<div class="modal-overlay" id="createTournamentModal">')
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected successfully.")
else:
    print("Already exists.")
