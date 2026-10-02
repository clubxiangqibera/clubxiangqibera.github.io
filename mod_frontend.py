import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Payment Receipt Upload
target_pay = '''<td><button class="btn-sm green" onclick="markPaid('${s.id}')">核准已缴</button></td>'''
replacement_pay = '''<td>
        <div style="display:flex; gap:4px; justify-content:center;">
          <button class="btn-sm green" onclick="markPaid('${s.id}')">核准已缴</button>
          <button class="btn-sm" style="background:var(--pri3); color:#fff; border:none;" onclick="document.getElementById('receiptUpload_${s.id}').click()">上传凭证</button>
          <input type="file" id="receiptUpload_${s.id}" style="display:none;" accept="image/*" onchange="uploadReceiptFile('${s.id}', this)">
        </div>
      </td>'''
text = text.replace(target_pay, replacement_pay)

# Match Photo Upload
target_match = '''<div onclick="triggerUploadMatchPhoto('${m.date}','${m.round}','${m.red}','${m.black}')" style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">暂无实体记谱纸照片</div>'''
replacement_match = '''<div onclick="document.getElementById('matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()" style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">上传实体记谱纸照片</div>
      <input type="file" id="matchPhotoUpload_${m.date}_${m.round}_${m.red}_${m.black}" style="display:none;" accept="image/*" onchange="uploadMatchPhotoFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">'''
text = text.replace(target_match, replacement_match)

# And if they used the other template (if it had 暂无 in the text)
# Wait, in the user's screenshot it says "暂无实体记谱纸照片" which is just text, they want to click it.
# So I should make sure I replace the text correctly.
# Let's check the exact string:
exact_target_match = '''<div style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);">暂无实体记谱纸照片</div>'''
exact_replacement_match = '''<div onclick="document.getElementById('matchPhotoUpload_${idx}').click()" style="padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">上传实体记谱纸照片</div>
      <input type="file" id="matchPhotoUpload_${idx}" style="display:none;" accept="image/*" onchange="uploadMatchPhotoFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">'''
text = text.replace(exact_target_match, exact_replacement_match)


js_functions = '''
async function uploadReceiptFile(studentId, inputEl) {
  if (!inputEl.files || inputEl.files.length === 0) return;
  const file = inputEl.files[0];
  const ogText = inputEl.previousElementSibling.innerHTML;
  inputEl.previousElementSibling.innerHTML = '上传中...';
  inputEl.previousElementSibling.disabled = true;
  
  try {
    const base64 = await compressImage(file);
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'uploadReceipt', studentId: studentId, receiptImage: base64 })
    });
    const data = await res.json();
    if(data.success) {
      toast('凭证上传成功', 'success');
      loadAllData(); // Reload to show updated status
    } else {
      toast('上传失败: ' + (data.error||''), 'error');
    }
  } catch (e) {
    toast('网络错误', 'error');
  }
  inputEl.previousElementSibling.innerHTML = ogText;
  inputEl.previousElementSibling.disabled = false;
  inputEl.value = '';
}

async function uploadMatchPhotoFile(date, round, redName, blackName, inputEl) {
  if (!inputEl.files || inputEl.files.length === 0) return;
  const file = inputEl.files[0];
  const ogText = inputEl.previousElementSibling.innerHTML;
  inputEl.previousElementSibling.innerHTML = '上传中...';
  
  try {
    const base64 = await compressImage(file);
    const res = await fetch(GAS_API_URL, {
      method: 'POST',
      body: JSON.stringify({ action: 'updateMatchPhoto', date: date, round: round, redName: redName, blackName: blackName, imageBase64: base64 })
    });
    const data = await res.json();
    if(data.success) {
      toast('记谱纸上传成功', 'success');
      loadMatches(); // Reload matches
    } else {
      toast('上传失败: ' + (data.error||''), 'error');
    }
  } catch (e) {
    toast('网络错误', 'error');
  }
  inputEl.previousElementSibling.innerHTML = ogText;
  inputEl.value = '';
}
'''

text = text.replace('function renderStudentTables(){', js_functions + '\nfunction renderStudentTables(){')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated frontend!')
