import re

for file in ['admin.html', 'school.html']:
    html = open(file, encoding='utf-8').read()
    
    # Let's insert a call to translate [data-i18n] directly inside changeGlobalLang
    # Look for 'function changeGlobalLang(lang) {'
    replacement = r'''function changeGlobalLang(lang) {
  // Translate nav-adapter elements
  let navLang = lang === 'zh' ? 'cn' : lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    if(typeof i18n !== 'undefined' && i18n[navLang] && i18n[navLang][el.getAttribute('data-i18n')]) {
      el.innerHTML = i18n[navLang][el.getAttribute('data-i18n')];
    }
  });
  if(typeof updateSeg === 'function') updateSeg(navLang);
'''
    html = re.sub(r'function changeGlobalLang\(lang\) \{', replacement, html)
    
    open(file, 'w', encoding='utf-8').write(html)
    print(f'Patched init in {file}')
