import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove background and color from #securityGate
new_css = """#securityGate {
      display: flex; flex-direction: column; align-items: center;
      width: 100%; min-height: 100vh; padding: 0;
    }"""

text = re.sub(r'#securityGate\s*\{[^}]*\}', new_css, text)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed securityGate CSS')
