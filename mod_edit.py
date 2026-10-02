import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add an Edit button to the card in renderEvents
old_card_buttons = '''        <button onclick="deleteEvent(${idx})" class="btn" style="width:100%; padding:6px; background:#FDEDEC; color:#E74C3C; border:none; border-radius:8px; font-weight:700;">删除图集</button>'''

new_card_buttons = '''        <div style="display:flex; gap:8px;">
          <button onclick="editEvent(${idx})" class="btn" style="flex:1; padding:6px; background:#E8F8F5; color:#1ABC9C; border:none; border-radius:8px; font-weight:700;">编辑</button>
          <button onclick="deleteEvent(${idx})" class="btn" style="flex:1; padding:6px; background:#FDEDEC; color:#E74C3C; border:none; border-radius:8px; font-weight:700;">删除</button>
        </div>'''

text = text.replace(old_card_buttons, new_card_buttons)

# Add the JS function for editEvent
js_edit = '''
async function editEvent(idx) {
  const evt = window._events[idx];
  const newName = prompt('修改活动名称：', evt.name);
  if (newName === null) return;
  const newDate = prompt('修改活动日期 (YYYY-MM-DD)：', evt.date);
  if (newDate === null) return;
  const newDesc = prompt('修改简短描述：', evt.desc || '');
  if (newDesc === null) return;
  
  evt.name = newName.trim() || evt.name;
  evt.date = newDate.trim() || evt.date;
  evt.desc = newDesc.trim();
  
  const events = [...window._events];
  try {
    const res = await fetch('https://cxb-license.clubxiangqibera.workers.dev/api/admin/events', {
      method: 'POST',
      body: JSON.stringify({ adminPin: getAuthPin(), events: events })
    });
    if((await res.json()).success) {
      if(typeof toast === 'function') toast('已更新', 'success');
      window._events = events;
      renderEvents();
    }
  } catch(e) {}
}

function compressImage'''

text = text.replace('function compressImage', js_edit)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Edit button injected!")
