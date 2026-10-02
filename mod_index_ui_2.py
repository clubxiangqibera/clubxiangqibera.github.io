import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check toggle sidebar function
for m in re.finditer(r'<button class="menu-toggle" onclick="([^"]+)">', text):
    print("Toggle function is:", m.group(1))
    func_name = m.group(1).split('(')[0]
    # find definition
    idx = text.find('function ' + func_name)
    if idx != -1:
        print(text[idx:idx+200])

# 2. Update .icon-circle
icon_idx = text.find('.icon-circle{')
if icon_idx != -1:
    print("Found .icon-circle{")
    end_idx = text.find('}', icon_idx)
    old_css = text[icon_idx:end_idx+1]
    new_css = """.icon-circle{
      width:52px;height:52px;border-radius:16px;display:flex;align-items:center;
      justify-content:center;font-size:24px;margin-bottom:6px;color:var(--primary-light);
      background: linear-gradient(135deg, rgba(41,128,185,0.1), rgba(14,47,68,0.05));
      border: 1.5px solid var(--border);
      transition: all 0.2s ease;
    }
    .icon-item:hover .icon-circle {
      transform: scale(1.1);
      background: linear-gradient(135deg, var(--primary-light), var(--primary-mid));
      border-color: transparent;
      box-shadow: 0 6px 20px rgba(41,128,185,0.3);
    }
    .icon-item:hover .icon-circle span,
    .icon-item:hover .icon-label { color: var(--primary-light); }"""
    text = text.replace(old_css, new_css)
    print("Replaced .icon-circle")

# 3. Toggle sidebar overlay logic
toggle_func = """function toggleMenu(){
  const sb = document.querySelector('.app-sidebar');
  const ov = document.getElementById('sidebarOverlay');
  if(sb.style.transform === 'translateX(0px)'){
    sb.style.transform = 'translateX(-100%)';
    if(ov) ov.classList.remove('show');
  }else{
    sb.style.transform = 'translateX(0px)';
    if(ov) ov.classList.add('show');
  }
}"""
if 'function toggleMenu()' in text:
    old_toggle = re.search(r'function toggleMenu\(\)\{[\s\S]*?\}', text)
    if old_toggle:
        text = text.replace(old_toggle.group(0), toggle_func)
        print("Replaced toggleMenu()")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
