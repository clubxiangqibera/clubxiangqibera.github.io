import io
import re

with io.open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 11A. Add hover effect to table rows
if "table tbody tr {" not in text:
    text = text.replace('  </style>', '    table tbody tr { transition: background 0.15s; }\n    table tbody tr:hover { background: rgba(41,128,185,0.05); }\n  </style>')

# 11B. Style the XQF buttons nicely
if ".btn-sm.xqf" not in text:
    text = text.replace('  </style>', '    .btn-sm.xqf { background: #EBF5FB; color: var(--pri3); border-color: var(--pri3); }\n    .btn-sm.xqf:hover { background: var(--pri3); color: #fff; }\n  </style>')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("admin.html Task 11 done")

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix inline toggle
ov_logic = "function toggleSidebar(){ const sb = document.getElementById('appSidebar'); sb.classList.toggle('show'); const ov = document.getElementById('sidebarOverlay'); if(sb.classList.contains('show')){ ov.classList.add('show'); }else{ ov.classList.remove('show'); } }"
if "function toggleSidebar()" not in text:
    text = text.replace('</script>', ov_logic + '\n</script>')

text = text.replace("document.getElementById('appSidebar').classList.toggle('show')", "toggleSidebar()")

# Fix icon-circle
icon_old_match = re.search(r'\.icon-circle\s*\{[^\}]+\}', text)
if icon_old_match and 'display:flex' in icon_old_match.group(0):
    new_css = """.icon-circle{
      width:52px;height:52px;border-radius:16px;display:flex;align-items:center;
      justify-content:center;font-size:24px;margin-bottom:6px;color:var(--primary-light);
      background: linear-gradient(135deg, rgba(41,128,185,0.1), rgba(14,47,68,0.05));
      border: 1.5px solid var(--border);
      transition: all 0.2s ease;
    }
    .icon-item:hover .icon-circle {
      transform: scale(1.1);
      background: linear-gradient(135deg, var(--primary-light), var(--primary-mid));
      border-color: transparent;
      box-shadow: 0 6px 20px rgba(41,128,185,0.3);
    }
    .icon-item:hover .icon-circle span,
    .icon-item:hover .icon-label { color: var(--primary-light); }"""
    text = text.replace(icon_old_match.group(0), new_css)
    print("Replaced .icon-circle")

# Mobile sidebar fix for CSS
if '.sidebar-overlay' in text:
    # also add closing logic on clicking overlay
    text = text.replace('id="sidebarOverlay" onclick="toggleSidebar()"', 'id="sidebarOverlay" onclick="toggleSidebar()"')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
