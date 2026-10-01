import io
with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

old = '<td style="padding:10px 12px;font-size:12px;color:var(--text2);">${s.level}</td>'
new = '''<td style="padding:10px 12px;">
                <select id="acc_level_${i}" 
                  style="width:100%;padding:4px 6px;border:1.5px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg);"
                  onchange="autoSaveAccount(${i},'${s.id}',this)">
                  <option value="Lv 1 启蒙班" ${s.level==='Lv 1 启蒙班'?'selected':''}>Lv 1 启蒙班</option>
                  <option value="Lv 2 进阶班" ${s.level==='Lv 2 进阶班'?'selected':''}>Lv 2 进阶班</option>
                  <option value="Lv 3 精英班" ${s.level==='Lv 3 精英班'?'selected':''}>Lv 3 精英班</option>
                  <option value="非本会学员" ${s.level==='非本会学员'?'selected':''}>非本会学员</option>
                </select>
              </td>'''
text = text.replace(old, new)

old_save = '''const newName = document.getElementById(`acc_name_${idx}`).value.trim();
  const newPwd  = document.getElementById(`acc_pwd_${idx}`).value.trim();
  if (!newName || !newPwd) return;'''
new_save = '''const newName = document.getElementById(`acc_name_${idx}`).value.trim();
  const newPwd  = document.getElementById(`acc_pwd_${idx}`).value.trim();
  const newLevelEl = document.getElementById(`acc_level_${idx}`);
  const newLevel = newLevelEl ? newLevelEl.value : '';
  if (!newName || !newPwd) return;'''
text = text.replace(old_save, new_save)

old_fetch = "body: JSON.stringify({ action: 'updateAccount', studentId, newName, newPwd })"
new_fetch = "body: JSON.stringify({ action: 'updateAccount', studentId, newName, newPwd, newLevel })"
text = text.replace(old_fetch, new_fetch)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
