import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_render = re.search(r'function renderGallery\(\).*?\}\)\.join\(\'\'\);\n\}', text, re.DOTALL).group(0)

new_render = old_render.replace('return `', '''
    const hasXqf=m.xqfFile&&m.xqfFile.startsWith('http');
    const xqfBtn=hasXqf
      ?`<div onclick="window.open('${m.xqfFile}')" style="padding:12px;background:#EBF5FB;color:var(--pri3);font-size:12px;font-weight:700;text-align:center;cursor:pointer;border-top:1px solid var(--border);">💾 下载XQF电子棋谱</div>`
      :`<div onclick="document.getElementById('xqfUpload_${idx}').click()" style="padding:12px;text-align:center;font-size:11px;color:var(--text2);background:var(--bg);border-top:1px dashed var(--border);cursor:pointer;">📤 上传XQF电子棋谱</div>
      <input type="file" id="xqfUpload_${idx}" style="display:none;" accept=".xqf" onchange="uploadXqfFile('${m.date}','${m.round}','${m.red}','${m.black}', this)">`;
    return `''')

new_render = new_render.replace('${img}\n      </div>', '${img}\n        ${xqfBtn}\n      </div>')

text = text.replace(old_render, new_render)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated renderGallery')
