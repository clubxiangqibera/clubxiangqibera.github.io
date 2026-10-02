import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Create a new script block just for this.
js = '''
<script>
// --- MAIN NAV SYSTEM ---
function openMainNav() {
  const sidebar = document.getElementById('mainNavSidebar');
  const backdrop = document.getElementById('mainNavBackdrop');
  if(sidebar) sidebar.classList.add('open');
  if(backdrop) backdrop.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMainNav() {
  const sidebar = document.getElementById('mainNavSidebar');
  const backdrop = document.getElementById('mainNavBackdrop');
  if(sidebar) sidebar.classList.remove('open');
  if(backdrop) backdrop.classList.remove('open');
  document.body.style.overflow = '';
}
// --- END MAIN NAV SYSTEM ---
</script>
'''

# Inject before </body>
text = text.replace('</body>', js + '\n</body>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("JavaScript injected properly!")
