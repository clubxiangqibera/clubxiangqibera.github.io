import re

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    i18n_match = re.search(r'(const i18n = \{.*?\};)', index_html, re.DOTALL)
    if not i18n_match:
        print("Could not find i18n in index.html")
        return
        
    i18n_block = i18n_match.group(1)

    adapter_script = f'''
<script id="nav-adapter">
{i18n_block}

function togglePublicTab(tab) {{
  if (tab === 'home') window.location.href = 'index.html';
  else if (tab === 'ladder') window.location.href = 'index.html#ladder';
  else if (tab === 'login') window.location.href = 'index.html#login';
}}
function openArchiveView() {{
  window.location.href = 'index.html#events';
}}
function setLang(lang) {{
  let mapping = {{'cn': 'zh', 'bm': 'bm', 'en': 'en'}};
  let mapped = mapping[lang] || 'zh';
  if (typeof changeGlobalLang === 'function') {{
    changeGlobalLang(mapped);
  }} else if (typeof updateMenuI18n === 'function') {{
    updateMenuI18n(mapped);
  }}
  
  // also apply translations to the copied menu items
  let navLang = lang === 'zh' ? 'cn' : lang; // fallback if needed
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const key = el.getAttribute('data-i18n');
    if(i18n[navLang] && i18n[navLang][key]) {{
      if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
        el.placeholder = i18n[navLang][key];
      }} else {{
        el.innerHTML = i18n[navLang][key];
      }}
    }}
  }});
}}
function updateSeg(lang) {{
  document.querySelectorAll('.apple-segment .seg-btn').forEach(b => b.classList.remove('active'));
  let activeBtn = document.getElementById('seg_' + lang);
  if(activeBtn) activeBtn.classList.add('active');
}}
</script>
'''
    
    for file in ['admin.html', 'school.html']:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Replace the old adapter_script with this new one
        # I can just do a re.sub on the adapter script
        new_html, count = re.subn(r'<script id="nav-adapter">.*?</script>', adapter_script.replace('\\', '\\\\'), html, flags=re.DOTALL)
        
        if count > 0:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Updated adapter in {file} successfully.")
        else:
            print(f"Failed to find adapter in {file}")

run()
