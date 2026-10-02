import io, sys
sys.stdout.reconfigure(encoding='utf-8')

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

hash_handler = '''
window.addEventListener('DOMContentLoaded', () => {
  if (window.location.hash === '#login' || new URLSearchParams(window.location.search).get('tab') === 'login') {
    togglePublicTab('login');
  }
});
window.addEventListener('hashchange', () => {
  if (window.location.hash === '#login') {
    togglePublicTab('login');
  } else if (window.location.hash === '' || window.location.hash === '#home') {
    togglePublicTab('home');
  }
});
'''

text = text.replace('// --- END MAIN NAV SYSTEM ---', '// --- END MAIN NAV SYSTEM ---\n' + hash_handler)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("index.html hash routing added!")
