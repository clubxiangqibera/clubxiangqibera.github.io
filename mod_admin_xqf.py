import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the "暂无XQF棋谱" with an upload button
admin_old_xqf = "`<div style=\"padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);\">暂无XQF棋谱</div>`;"

admin_new_xqf = "`<div onclick=\"document.getElementById('xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}').click()\" style=\"padding:16px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;\">上传XQF电子棋谱</div>\n      <input type=\"file\" id=\"xqfUpload_${m.date}_${m.round}_${m.red}_${m.black}\" style=\"display:none;\" accept=\".xqf\" onchange=\"uploadXqfFile('${m.date}','${m.round}','${m.red}','${m.black}', this)\">`;"

if admin_old_xqf in text:
    text = text.replace(admin_old_xqf, admin_new_xqf)
else:
    print("Could not find admin_old_xqf")

# Add uploadXqfFile function in admin.html
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
        toast('XQF棋谱上传成功', 'success');
        loadAllData(); // Reload matches
      } else {
        toast('上传失败: ' + (data.error||''), 'error');
      }
    };
    reader.readAsDataURL(file);
  } catch (e) {
    toast('网络错误', 'error');
  }
  inputEl.previousElementSibling.innerHTML = ogText;
  inputEl.value = '';
}
"""

if 'uploadXqfFile' not in text:
    text = text.replace('async function uploadMatchPhotoFile', js_func + '\nasync function uploadMatchPhotoFile')
else:
    print("uploadXqfFile already exists")

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("admin.html updated successfully")
