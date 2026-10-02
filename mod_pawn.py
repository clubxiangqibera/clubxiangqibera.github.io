import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'aTitle' in l and 'Club XiangQi Bera' in l:
        print("Found title at line", i)
        lines[i-1] = '    <img src="cxb_round_emblem.png" alt="Logo" style="width:72px; height:72px; border-radius:50%; margin-bottom:16px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">\n'
        break

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done replacing.')
