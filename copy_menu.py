import re
import os

def run():
    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    nav_match = re.search(r'(<header class="public-nav-bar".*?</header>)', index_html, re.DOTALL)
    menu_match = re.search(r'(<!-- === APPLE STYLE MEGA MENU === -->.*?<div id="appleMegaBackdrop".*?</div>\s*</div>)', index_html, re.DOTALL)
    
    if not nav_match or not menu_match:
        print("Could not find nav or menu in index.html")
        return
        
    nav_block = nav_match.group(1)
    menu_block = menu_match.group(1)
    
    # We will inject the adapter script
    adapter_script = '''
<script id="nav-adapter">
function togglePublicTab(tab) {
  if (tab === 'home') window.location.href = 'index.html';
  else if (tab === 'ladder') window.location.href = 'index.html#ladder';
  else if (tab === 'login') window.location.href = 'index.html#login';
}
function openArchiveView() {
  window.location.href = 'index.html#events';
}
function setLang(lang) {
  let mapping = {'cn': 'zh', 'bm': 'bm', 'en': 'en'};
  let mapped = mapping[lang] || 'zh';
  if (typeof changeGlobalLang === 'function') {
    changeGlobalLang(mapped);
  } else if (typeof updateMenuI18n === 'function') {
    updateMenuI18n(mapped);
  }
}
function updateSeg(lang) {
  document.querySelectorAll('.apple-segment .seg-btn').forEach(b => b.classList.remove('active'));
  let activeBtn = document.getElementById('seg_' + lang);
  if(activeBtn) activeBtn.classList.add('active');
}
</script>
'''

    full_replacement = f"{nav_block}\n\n{menu_block}\n{adapter_script}"
    
    for file in ['admin.html', 'school.html']:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Replace the existing nav and menu in admin/school
        # We need a regex that captures from <header class="public-nav-bar"> up to the end of <div id="appleMegaMenu"...></div>
        
        # Actually, let's just do a greedy match from <header class="public-nav-bar"> to the end of appleMegaMenu
        # It's safer to match them separately or as a block if they are contiguous.
        # Let's check how they are structured in admin.html
        
        # In admin.html, it's:
        # <header class="public-nav-bar"> ... </header>
        # <!-- APPLE MEGA MENU & BACKDROP -->
        # <div id="appleMegaBackdrop"...
        # <div id="appleMegaMenu"...> ... </div>
        
        pattern = r'<header class="public-nav-bar".*?</header>.*?<div id="appleMegaBackdrop".*?</div>\s*</div>'
        
        new_html, count = re.subn(pattern, full_replacement, html, flags=re.DOTALL)
        
        if count == 0:
            print(f"Could not find replacement target in {file}")
            # Try a broader or different pattern
        else:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Updated {file} successfully.")

run()
