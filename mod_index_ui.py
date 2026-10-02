import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = "verdict: (r[7]||'').trim(), recordImg: (r[8]||'').trim()"
new_str = "verdict: (r[7]||'').trim(), recordImg: (r[8]||'').trim(), xqfFile: (r[9]||'').trim()"

if old_str in text:
    text = text.replace(old_str, new_str)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 1: Fixed xqfFile loading in index.html')
else:
    print('Task 1: old_str not found in index.html')

# TASK 3: Fix WhatsApp Placeholder
wa_old = "window.open('https://chat.whatsapp.com/your-group-link','_blank')"
wa_new = "window.open('https://wa.me/60123456789','_blank')"
if wa_old in text:
    text = text.replace(wa_old, wa_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 3: Fixed WhatsApp link')

# TASK 4B: Fix match cards white background in dark mode
mc_old = '<div class="match-card" style="border-left: 5px solid #F1C40F; background: #FFFCF2;">'
mc_new = '<div class="match-card" style="border-left: 5px solid #F1C40F;">'
if mc_old in text:
    text = text.replace(mc_old, mc_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 4B: Removed hardcoded background from match-card HTML')

mc_css_old = "    .match-card{\n      padding:14px;border-radius:14px;border:1.5px solid var(--border);\n      background:var(--card);display:flex;justify-content:space-between;align-items:center;\n      box-shadow:var(--shadow);\n    }"
mc_css_new = mc_css_old + "\n    @media(prefers-color-scheme:dark){\n      .match-card{ background: var(--card) !important; }\n    }"
if mc_css_old in text:
    text = text.replace(mc_css_old, mc_css_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 4B: Added dark mode match-card CSS')

# TASK 4C: Fix sidebar active link colors in dark mode
sb_old = ".sb-link:hover, .sb-link.active { background: var(--primary-light); color: var(--primary-dark); }"
sb_new = ".sb-link:hover, .sb-link.active { background: rgba(41,128,185,0.15); color: var(--primary-light); }"
if sb_old in text:
    text = text.replace(sb_old, sb_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 4C: Fixed sidebar active link color')

# TASK 4E: Fix logout button in dark mode
lo_old = ".sb-logout { margin-top: auto; padding: 12px 16px; border-radius: 10px; border:none; background: #FDEDEC; color: #E74C3C; font-weight: 800; cursor: pointer; text-align: left; }"
lo_new = lo_old + "\n    @media(prefers-color-scheme:dark){ .sb-logout { background: rgba(231,76,60,0.15); } }"
if lo_old in text:
    text = text.replace(lo_old, lo_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 4E: Fixed logout button dark mode')

# TASK 5A: Add CSS animation classes
anim_css = """    /* ANIMATIONS */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
      animation: fadeInUp 0.5s ease forwards;
      opacity: 0;
    }
    .animate-in:nth-child(1) { animation-delay: 0.05s; }
    .animate-in:nth-child(2) { animation-delay: 0.1s; }
    .animate-in:nth-child(3) { animation-delay: 0.15s; }
    .animate-in:nth-child(4) { animation-delay: 0.2s; }
    .animate-in:nth-child(5) { animation-delay: 0.25s; }
    .animate-in:nth-child(6) { animation-delay: 0.3s; }
    .animate-in:nth-child(7) { animation-delay: 0.35s; }
    .animate-in:nth-child(8) { animation-delay: 0.4s; }
"""
if "keyframes fadeInUp" not in text:
    text = text.replace("  </style>", anim_css + "  </style>")
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 5A: Added animation CSS')

# TASK 5B: Apply animation to quick menu icons
if 'class="icon-item"' in text:
    text = text.replace('class="icon-item"', 'class="icon-item animate-in"')
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 5B: Applied animation class to icon items')

# TASK 6A: Add sidebar overlay backdrop
overlay_css = """    .sidebar-overlay {
      display: none;
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.5); z-index: 199;
      backdrop-filter: blur(2px);
    }
    .sidebar-overlay.show { display: block; }
"""
if "sidebar-overlay" not in text:
    text = text.replace("  </style>", overlay_css + "  </style>")
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 6A: Added sidebar overlay CSS')

# TASK 6B: Add overlay div in HTML
ov_html = '  <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>\n'
if 'sidebarOverlay' not in text:
    text = text.replace('  </div> <!-- end sidebar -->', '  </div> <!-- end sidebar -->\n' + ov_html)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 6B: Added sidebar overlay HTML')

# TASK 6C: Update toggleSidebar function
ts_old = """function toggleSidebar() {
  const sb = document.querySelector('.app-sidebar');
  if (sb.style.transform === 'translateX(0px)') {
    sb.style.transform = 'translateX(-100%)';
  } else {
    sb.style.transform = 'translateX(0px)';
  }
}"""
ts_new = """function toggleSidebar() {
  const sb = document.querySelector('.app-sidebar');
  const ov = document.getElementById('sidebarOverlay');
  if (sb.style.transform === 'translateX(0px)') {
    sb.style.transform = 'translateX(-100%)';
    if(ov) ov.classList.remove('show');
  } else {
    sb.style.transform = 'translateX(0px)';
    if(ov) ov.classList.add('show');
  }
}"""
if ts_old in text:
    text = text.replace(ts_old, ts_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 6C: Updated toggleSidebar JS')
else:
    # try looser match
    import re
    ts_old_regex = re.compile(r'function toggleSidebar\(\) \{\s*const sb = document\.querySelector\(\'\.app-sidebar\'\);\s*if \(sb\.style\.transform === \'translateX\(0px\)\'\) \{\s*sb\.style\.transform = \'translateX\(-100%\)\';\s*\} else \{\s*sb\.style\.transform = \'translateX\(0px\)\';\s*\}\s*\}')
    if ts_old_regex.search(text):
        text = ts_old_regex.sub(ts_new, text)
        with io.open('index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Task 6C: Updated toggleSidebar JS (regex)')
    else:
        print('Task 6C: ts_old not found')

# TASK 7A: Add section header CSS
sec_css = """    .section-head {
      text-align: center; margin-bottom: 24px; padding: 0 16px;
    }
    .section-title {
      font-size: 20px; font-weight: 900; color: var(--text);
    }
    .section-sub {
      font-size: 13px; color: var(--text2); margin-top: 4px;
    }
"""
if ".section-head {" not in text:
    text = text.replace("  </style>", sec_css + "  </style>")
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 7A: Added section header CSS')

# TASK 8A: Add subtle gradient border to hero card
hero_css_old = """    .student-hero{
      background:linear-gradient(135deg,var(--primary),var(--primary-mid));
      color:#fff;border-radius:var(--radius);padding:24px;
      display:flex;align-items:center;gap:18px;margin-bottom:24px;
      box-shadow:0 8px 30px rgba(14,47,68,0.25);
    }"""
hero_css_new = """    .student-hero{
      background:linear-gradient(135deg,var(--primary),var(--primary-mid));
      color:#fff;border-radius:var(--radius);padding:24px;
      display:flex;align-items:center;gap:18px;margin-bottom:24px;
      box-shadow:0 8px 30px rgba(14,47,68,0.25);
      position: relative; overflow: hidden;
    }
    .student-hero::before {
      content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
      background: linear-gradient(135deg, rgba(243,156,18,0.4), rgba(41,128,185,0.4));
      border-radius: 22px; z-index: -1;
    }"""
if "background:linear-gradient(135deg,var(--primary),var(--primary-mid));" in text and ".student-hero::before" not in text:
    text = text.replace(hero_css_old, hero_css_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 8A: Added student-hero gradient glow')

# TASK 9A: Polish Icon Grid (Quick Menu)
icon_css_old = """    .icon-circle{
      width:48px;height:48px;border-radius:14px;background:rgba(41,128,185,0.1);
      display:flex;align-items:center;justify-content:center;
      font-size:22px;margin-bottom:6px;color:var(--primary-light);
    }"""
icon_css_new = """    .icon-circle{
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
if "width:48px;height:48px;border-radius:14px;" in text:
    text = text.replace(icon_css_old, icon_css_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 9A: Updated icon-circle CSS')
else:
    print('Task 9A: icon_css_old not found')

# TASK 10A: Improve Public Leaderboard Cards
rank_css_old = """    .rank-card{
      background:var(--card);border-radius:14px;padding:16px;
      display:flex;align-items:center;gap:14px;
      border:1px solid var(--border);box-shadow:var(--shadow);
    }"""
rank_css_new = """    .rank-card{
      background:var(--card);border-radius:14px;padding:16px;
      display:flex;align-items:center;gap:14px;
      border:1px solid var(--border);box-shadow:var(--shadow);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .rank-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }"""
if rank_css_old in text:
    text = text.replace(rank_css_old, rank_css_new)
    with io.open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Task 10A: Updated rank-card hover CSS')
else:
    print('Task 10A: rank_css_old not found')

