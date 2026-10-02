import io
import re

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# The original HTML for the button:
# <a href="https://chat.whatsapp.com/your-group-link" target="_blank" class="btn-wa">
#   📲 立即报名 WhatsApp
# </a>

text = re.sub(
    r'<a href="https://chat\.whatsapp\.com[^"]*" target="_blank" class="btn-wa">.*?</a>',
    '<a href="https://forms.gle/KUQu7MkUYLnvYeSd6" target="_blank" class="btn-wa" style="background:#4285F4;box-shadow: 0 6px 16px rgba(66,133,244,0.3);">\n            📝 立即填写 Google Form 报名表\n          </a>',
    text,
    flags=re.DOTALL
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Replaced")
