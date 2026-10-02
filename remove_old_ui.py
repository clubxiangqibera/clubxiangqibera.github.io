import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

old = '''// Teacher PIN editor
  el.innerHTML = `
    <div style="background:rgba(41,128,185,0.08);border:1.5px solid rgba(41,128,185,0.3);border-radius:14px;padding:16px;margin-bottom:20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
      <div style="font-size:14px;font-weight:900;color:#2980B9;flex-shrink:0;">🎓 设置教练密码 (Set Coach PIN)</div>
      <input type="password" id="coachPinInput" placeholder="新密码" maxlength="16"
        style="width:140px;padding:8px 12px;border:1.5px solid rgba(41,128,185,0.4);border-radius:10px;font-size:16px;font-weight:900;text-align:center;background:#fff;"
        onblur="saveCoachPin(this.value)" oninput="this.style.borderColor='#F39C12'">
      <span style="font-size:12px;color:var(--text2);">输入后点击空白处保存 · 状态: <strong id="coachPinDisplay">********</strong></span>
    </div>

    <div style="overflow-x:auto;">'''

new = '''// Teacher PIN editor removed (moved to coach list UI)
  el.innerHTML = `
    <div style="overflow-x:auto;">'''

text = text.replace(old, new)

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Replaced")
