import io

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace pawn with logo
text = text.replace('<div style="font-size:42px; margin-bottom:12px;">♟️</div>', 
                    '<img src="cxb_round_emblem.png" alt="Logo" style="width:72px; height:72px; border-radius:50%; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">')

# Center the lang switch in login screen
# Wait, .lang-switch-wrap might be used globally in admin.html, let's check
if '.lang-switch-wrap{display:flex;justify-content:flex-end;margin-bottom:12px;}' in text.replace(' ', ''):
    pass
# I will just inline style it for the login screen to be sure
target = '<div class="lang-switch-wrap">'
text = text.replace(target, '<div class="lang-switch-wrap" style="justify-content:center; margin-bottom:20px;">')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated login screen")
