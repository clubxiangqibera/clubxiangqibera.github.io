import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the JavaScript not being injected
js = '''
// --- MAIN NAV SYSTEM ---
function openMainNav() {
  document.getElementById('mainNavSidebar').classList.add('open');
  document.getElementById('mainNavBackdrop').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMainNav() {
  document.getElementById('mainNavSidebar').classList.remove('open');
  document.getElementById('mainNavBackdrop').classList.remove('open');
  document.body.style.overflow = '';
}
// --- END MAIN NAV SYSTEM ---
</script>'''

# Inject before the final </script> block for the body
text = re.sub(r'</script>\s*</body>', js + '\n</body>', text, count=1)

# 2. Fix the button styling (remove btn--primary)
old_btn = r'<button class="btn btn--primary" style="padding: 10px 18px; font-size: 14px; display:flex; gap:8px; align-items:center;" onclick="openMainNav\(\)">'
new_btn = r'<button class="nav-menu-btn" onclick="openMainNav()">'
text = re.sub(old_btn, new_btn, text)

# Inject the CSS for .nav-menu-btn
css = '''
.nav-menu-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: #fff;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  gap: 8px;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}
.nav-menu-btn:hover {
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(241, 196, 15, 0.1);
}
</style>'''
text = text.replace('</style>', css, 1)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Button fixed and JS injected!")
