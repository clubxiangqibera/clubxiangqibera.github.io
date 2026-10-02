import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_gallery = re.search(r'<!-- 4\. EVENTS GALLERY -->.*?<div id="publicGalleryArea".*?</div>\s*</div>\s*</div>', text, flags=re.DOTALL)
if not old_gallery:
    old_gallery = re.search(r'<!-- 4\. EVENTS GALLERY -->.*?<div id="publicGalleryArea".*?</div>\s*</div>', text, flags=re.DOTALL)
    
if old_gallery:
    new_events_section = '''<!-- 4. SUPER EVENT SYSTEM -->
      <section class="section" id="events" style="margin-top: 40px;">
        <div class="section__head">
          <h2 class="section__title" data-i18n="events.title">赛事与活动中心</h2>
          <p class="section__sub" data-i18n="events.sub">记录百乐县中国象棋公会的精彩瞬间与赛事资源</p>
        </div>
        <div id="homeEventsGrid" class="events-grid"></div>
        <div style="text-align: center; margin-top: 36px;">
          <button class="btn btn--ghost" onclick="openArchiveView()">
            📚 查看所有历届活动 / View All Events
          </button>
        </div>
      </section>'''
    text = text.replace(old_gallery.group(0), new_events_section)
    print("Replaced successfully")
else:
    print("STILL NOT FOUND")

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
