import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# I need to revert my previous change for 'paymentTable' and replace it with the new logic.
# Wait, I previously injected:
old_html = '''<div style="display:flex; gap:4px; justify-content:center;">
          <button class="btn-sm green" onclick="markPaid('${s.id}')">核准已缴</button>
          <button class="btn-sm" style="background:var(--pri3); color:#fff; border:none;" onclick="document.getElementById('receiptUpload_${s.id}').click()">上传凭证</button>
          <input type="file" id="receiptUpload_${s.id}" style="display:none;" accept="image/*" onchange="uploadReceiptFile('${s.id}', this)">
        </div>'''

# I will find the paymentTable mapping function
match = re.search(r"document\.getElementById\('paymentTable'\)\.innerHTML=allStudents\.map\(s=>\n\s*`(.*?)`\n\s*\)\.join\(''\);", text, re.DOTALL)
if match:
    row_html = match.group(1)
    
    # Let's replace the whole assignment
    new_assignment = '''document.getElementById('paymentTable').innerHTML=allStudents.map(s=>{
    const parts = s.payStatus.split('|');
    const statusText = parts[0];
    const imgUrl = parts[1] || '';
    return `<tr><td><strong>${s.id}</strong></td><td>${s.cnName}</td><td>${s.level}</td><td>${s.feeMode}</td><td>${s.comboExpiry||'-'}</td><td>${payBadge(statusText)}</td>
      <td>
        <div style="display:flex; gap:4px; justify-content:center;">
          <button class="btn-sm green" onclick="markPaid('${s.id}')">核准已缴</button>
          ${imgUrl ? `<button class="btn-sm" style="background:#F39C12; color:#fff; border:none;" onclick="openLightbox('${imgUrl}')">查看凭证</button>` : ''}
        </div>
      </td></tr>`;
  }).join('');'''
    
    text = text.replace(match.group(0), new_assignment)
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced paymentTable mapping!")
else:
    print("Could not find paymentTable mapping")

