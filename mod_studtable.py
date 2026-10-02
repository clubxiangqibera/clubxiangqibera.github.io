import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace studentTable mapping to also split payStatus
match = re.search(r"document\.getElementById\('studentTable'\)\.innerHTML=allStudents\.map\(s=>\n\s*`(.*?)`\n\s*\)\.join\(''\);", text, re.DOTALL)
if match:
    new_assignment = '''document.getElementById('studentTable').innerHTML=allStudents.map(s=>{
    const parts = s.payStatus.split('|');
    const statusText = parts[0];
    return `<tr>
      <td><strong>${s.id}</strong></td>
      <td><strong>${s.cnName}</strong></td>
      <td>${s.enName||'-'}</td>
      <td>${s.gender}</td>
      <td>${s.school}</td>
      <td><span class="badge badge-blue">${s.level}</span></td>
      <td>${s.elo}</td>
      <td>${payBadge(statusText)}</td>
      <td style="text-align:center;">
        <button class="btn-sm" style="color:var(--red);border-color:var(--red);padding:4px 8px;font-size:11px;" onclick="deleteStudentAccount('${s.id}','${s.cnName}')">🗑️ 移除</button>
      </td>
    </tr>`;
  }).join('');'''
    
    text = text.replace(match.group(0), new_assignment)
    with io.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced studentTable mapping!")
else:
    print("Could not find studentTable mapping")

