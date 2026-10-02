import io, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Restore the ladder HTML
ladder_html = '''

      <!-- 5. LADDER (REAL-TIME) -->
      <section class="section" id="ladder">
        <div class="section__head">
          <h2 class="section__title" id="podiumHeader" data-i18n="ladder.title">百乐全县青少年天梯排位</h2>
          <p class="section__sub" data-i18n="ladder.sub">CXQB ELO 官方排位体系 · 实时同步</p>
        </div>
        <div id="publicPodiumArea"></div>
      </section>
'''

# Find the end of the events section
idx = text.find('</section>', text.find('id="events"'))
if idx != -1:
    text = text[:idx+10] + ladder_html + text[idx+10:]
    
with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Ladder restored.")
