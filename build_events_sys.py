import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace Gallery HTML with Events Hub HTML
old_gallery = re.search(r'<section class="section" id="gallery">.*?</section>', text, flags=re.DOTALL)
if old_gallery:
    new_events_section = '''<section class="section" id="events">
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
else:
    print("Could not find gallery section")

# 2. Add CSS
css_additions = '''
/* --- Super Event System --- */
.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}
.event-card {
  background: var(--navy-900);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: flex; flex-direction: column;
}
.event-card:hover {
  transform: translateY(-4px);
  border-color: var(--gold);
}
.event-card__cover {
  width: 100%; height: 180px;
  background-color: var(--navy-800);
  background-size: cover; background-position: center;
  border-bottom: 1px solid var(--line);
}
.event-card__body { padding: 24px; flex: 1; display: flex; flex-direction: column; }
.event-card__date { font-size: 0.85rem; color: var(--gold-soft); margin-bottom: 8px; font-weight: 600; letter-spacing: 0.05em; }
.event-card__title { font-size: 1.25rem; color: var(--ink); font-weight: 700; margin-bottom: 12px; line-height: 1.4; font-family: var(--font-serif); }
.event-card__desc { font-size: 0.9rem; color: var(--ink-dim); line-height: 1.6; margin-bottom: 0; margin-top: auto; }

/* Detail Modal */
.evt-modal {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(7, 16, 30, 0.95); backdrop-filter: blur(8px);
  display: none; align-items: center; justify-content: center;
  padding: 20px;
}
.evt-modal__content {
  background: var(--navy-900);
  width: 100%; max-width: 760px; max-height: 90vh;
  border: 1px solid var(--gold); border-radius: var(--radius);
  overflow-y: auto; position: relative;
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}
.evt-modal__close {
  position: absolute; top: 16px; right: 16px;
  background: rgba(0,0,0,0.6); color: #fff; border: 1px solid var(--line);
  border-radius: 50%; width: 36px; height: 36px;
  cursor: pointer; font-size: 18px; z-index: 10;
  display: flex; align-items: center; justify-content: center;
}
.evt-modal__close:hover { background: var(--red); border-color: var(--red); }
.evt-modal__cover { width: 100%; height: 280px; background-size: cover; background-position: center; border-bottom: 1px solid var(--gold); }
.evt-modal__body { padding: 40px; }
.evt-modal__title { font-size: 1.8rem; color: var(--gold); font-family: var(--font-serif); margin-bottom: 12px; line-height: 1.3; }
.evt-modal__date { font-size: 0.95rem; color: var(--ink-dim); margin-bottom: 24px; font-weight: 600; letter-spacing: 0.05em; }
.evt-modal__desc { font-size: 1rem; color: var(--ink); line-height: 1.8; margin-bottom: 36px; }

.evt-section-title { font-size: 1.15rem; color: var(--gold-soft); margin-bottom: 16px; border-bottom: 1px dashed var(--line); padding-bottom: 10px; font-weight: 700; }
.evt-links { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 36px; }
.evt-link-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px; font-size: 0.9rem; font-weight: 600;
  background: var(--navy-800); border: 1px solid var(--line); border-radius: 8px;
  color: var(--ink); cursor: pointer; text-decoration: none; transition: 0.2s;
}
.evt-link-btn:hover { border-color: var(--gold); color: var(--gold); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(201,162,75,0.1); }
.evt-gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 16px; margin-bottom: 36px; }
.evt-gallery img { width: 100%; height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid var(--line); cursor: pointer; transition: 0.2s; }
.evt-gallery img:hover { border-color: var(--gold); transform: scale(1.03); }

/* Full Archive View (Another Page Feel) */
.archive-view {
  position: fixed; inset: 0; z-index: 8000;
  background: var(--navy-950);
  overflow-y: auto; display: none;
}
.archive-view__header {
  position: sticky; top: 0; background: rgba(7, 16, 30, 0.95); backdrop-filter: blur(10px);
  padding: 20px clamp(20px, 5vw, 40px); border-bottom: 1px solid var(--line);
  display: flex; align-items: center; justify-content: space-between; z-index: 10;
}
.archive-view__title { font-size: 1.4rem; color: var(--gold); font-family: var(--font-serif); font-weight: 700; }
.archive-view__close {
  background: transparent; color: var(--ink); border: 1px solid var(--line);
  padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 0.95rem; font-weight: 600; transition: 0.2s;
}
.archive-view__close:hover { background: var(--navy-800); border-color: var(--gold); color: var(--gold); }
.archive-view__body { padding: 40px clamp(20px, 5vw, 40px); max-width: 1200px; margin: 0 auto; }
'''
text = text.replace('</style>', css_additions + '\n</style>')

# 3. Add HTML Modals
html_modals = '''
<!-- === ARCHIVE VIEW (The "Another Page") === -->
<div id="eventsArchiveView" class="archive-view">
  <div class="archive-view__header">
    <div class="archive-view__title">📚 历届活动总览 (Events Archive)</div>
    <button class="archive-view__close" onclick="closeArchiveView()">⬅ 返回首页 (Back)</button>
  </div>
  <div class="archive-view__body">
    <div id="archiveEventsGrid" class="events-grid"></div>
  </div>
</div>

<!-- === EVENT DETAIL MODAL === -->
<div id="eventDetailModal" class="evt-modal" onclick="if(event.target===this) closeEventDetail()">
  <div class="evt-modal__content">
    <button class="evt-modal__close" onclick="closeEventDetail()">×</button>
    <div id="evtModalCover" class="evt-modal__cover"></div>
    <div class="evt-modal__body">
      <div id="evtModalDate" class="evt-modal__date"></div>
      <h2 id="evtModalTitle" class="evt-modal__title"></h2>
      <div id="evtModalDesc" class="evt-modal__desc"></div>
      
      <div id="evtSectionFiles" style="display:none;">
        <div class="evt-section-title">📄 文件与简章 (Files & Documents)</div>
        <div id="evtModalFiles" class="evt-links"></div>
      </div>
      
      <div id="evtSectionResults" style="display:none;">
        <div class="evt-section-title">🏆 比赛成绩 (Results & Standings)</div>
        <div id="evtModalResults" style="margin-bottom: 36px; overflow-x:auto;"></div>
      </div>
      
      <div id="evtSectionPhotos" style="display:none;">
        <div class="evt-section-title">📸 活动图集 (Gallery)</div>
        <div id="evtModalPhotos" class="evt-gallery"></div>
      </div>

      <div id="evtSectionLinks" style="display:none;">
        <div class="evt-section-title">🔗 外部链接 (External Links)</div>
        <div id="evtModalLinks" class="evt-links" style="margin-bottom: 0;"></div>
      </div>
    </div>
  </div>
</div>
'''
text = text.replace('</body>', html_modals + '\n</body>')

# 4. Remove old loadPublicEvents JS and insert new super event system JS
old_gallery_js = re.search(r'// --- Public Gallery JS ---.*?// --- End Public Gallery JS ---', text, flags=re.DOTALL)
if old_gallery_js:
    text = text.replace(old_gallery_js.group(0), '')
else:
    print("Could not find old gallery JS")

super_event_js = '''
// --- SUPER EVENT SYSTEM ---
const mockEvents = [
  {
    id: 'evt-003',
    title: '2026 第一届「棋缘」中国象棋启蒙教育营',
    date: '2026-11-22',
    cover: 'poster_qiyuan_final.jpg',
    shortDesc: '百乐县首个面向零基础学员的象棋启蒙教育营，全套教材与专业教练指导。',
    fullDesc: '本届「棋缘」教育营由百乐象棋俱乐部主办。旨在发掘新生代象棋人才，为对中国象棋感兴趣的中小学生提供系统化的启蒙指导。<br><br>课程涵盖基础走法、杀局演练与残局破解。参与者不仅可获得全套教材，结业后还将获颁官方认证的结业证书。',
    photos: ['poster_qiyuan_final.jpg', 'persatuan_emblem.png'],
    files: [
      { label: '📄 教育营简章 (PDF)', url: '#' },
      { label: '📋 课程时间表', url: '#' }
    ],
    results: '',
    links: [
      { label: '🌐 前往 Google Form 报名', url: 'https://forms.gle/KUQu7MkUYLnvYeSd6' }
    ]
  },
  {
    id: 'evt-002',
    title: '2025年百乐县中小学象棋锦标赛',
    date: '2025-05-20',
    cover: 'cxb_round_emblem.png',
    shortDesc: '全县最大型的校际象棋比赛，共吸引了80名中小学生参与角逐。',
    fullDesc: '本次锦标赛在 Dewan SJK(C) Triang 1 隆重举行。来自全县12所学校的80名代表在棋盘上斗智斗勇，最终决出了各组别的冠亚季军。<br><br>比赛全程采用瑞士积分制，并引入了 CXQB ELO 等级分系统，极大地提升了比赛的专业性和激烈程度。',
    photos: [],
    files: [
      { label: '📄 比赛秩序册 (PDF)', url: '#' },
      { label: '📊 参赛选手名单', url: '#' }
    ],
    results: `<table class="table" style="width:100%; border:1px solid var(--line);">
                <thead><tr><th>名次</th><th>姓名</th><th>学校</th><th>积分</th></tr></thead>
                <tbody>
                  <tr><td>🥇 冠军</td><td>林家豪</td><td>SMJK Triang</td><td>6.0</td></tr>
                  <tr><td>🥈 亚军</td><td>黄梓轩</td><td>SJK(C) Triang (2)</td><td>5.5</td></tr>
                  <tr><td>🥉 季军</td><td>郭雨涵</td><td>SJK(C) Ladang Menteri</td><td>5.0</td></tr>
                  <tr><td>4th</td><td>陈美仪</td><td>SJK(C) Mengkarak</td><td>4.5</td></tr>
                </tbody>
              </table>`,
    links: [
      { label: '🔗 查看 Facebook 赛事报道', url: '#' }
    ]
  },
  {
    id: 'evt-001',
    title: '2024年 俱乐部挂牌成立大典',
    date: '2024-12-10',
    cover: 'persatuan_emblem.png',
    shortDesc: '历史性的一刻！百乐象棋俱乐部正式挂牌成立，并举办了首届会员内部交流赛。',
    fullDesc: '百乐象棋俱乐部正式成立，标志着百乐县中国象棋运动迈入了系统化、正规化的新纪元。理事会成员、地方长官与主要赞助商齐聚一堂，共同见证了揭牌仪式。<br><br>开幕典礼后，现场还举行了首届会员交流赛，气氛热烈。',
    photos: ['cxb_round_emblem.png'],
    files: [],
    results: '',
    links: []
  }
];

function renderEventCards(events, containerId) {
  const container = document.getElementById(containerId);
  if(!container) return;
  container.innerHTML = events.map(evt => `
    <div class="event-card" onclick="openEventDetail('${evt.id}')">
      <div class="event-card__cover" style="background-image: url('${evt.cover}')"></div>
      <div class="event-card__body">
        <div class="event-card__date">📅 ${evt.date}</div>
        <div class="event-card__title">${evt.title}</div>
        <div class="event-card__desc">${evt.shortDesc}</div>
      </div>
    </div>
  `).join('');
}

function openArchiveView() {
  document.getElementById('eventsArchiveView').style.display = 'block';
  document.body.style.overflow = 'hidden';
  renderEventCards(mockEvents, 'archiveEventsGrid');
}

function closeArchiveView() {
  document.getElementById('eventsArchiveView').style.display = 'none';
  document.body.style.overflow = '';
}

function openEventDetail(id) {
  const evt = mockEvents.find(e => e.id === id);
  if(!evt) return;

  document.getElementById('evtModalCover').style.backgroundImage = `url('${evt.cover}')`;
  document.getElementById('evtModalTitle').innerText = evt.title;
  document.getElementById('evtModalDate').innerText = '📅 ' + evt.date;
  document.getElementById('evtModalDesc').innerHTML = evt.fullDesc;

  // Files
  const filesArea = document.getElementById('evtModalFiles');
  if(evt.files && evt.files.length > 0) {
    filesArea.innerHTML = evt.files.map(f => `<a href="${f.url}" target="_blank" class="evt-link-btn">${f.label}</a>`).join('');
    document.getElementById('evtSectionFiles').style.display = 'block';
  } else {
    document.getElementById('evtSectionFiles').style.display = 'none';
  }

  // Links
  const linksArea = document.getElementById('evtModalLinks');
  if(evt.links && evt.links.length > 0) {
    linksArea.innerHTML = evt.links.map(f => `<a href="${f.url}" target="_blank" class="evt-link-btn">${f.label}</a>`).join('');
    document.getElementById('evtSectionLinks').style.display = 'block';
  } else {
    document.getElementById('evtSectionLinks').style.display = 'none';
  }

  // Results
  const resArea = document.getElementById('evtModalResults');
  if(evt.results) {
    resArea.innerHTML = evt.results;
    document.getElementById('evtSectionResults').style.display = 'block';
  } else {
    document.getElementById('evtSectionResults').style.display = 'none';
  }

  // Photos
  const photoArea = document.getElementById('evtModalPhotos');
  if(evt.photos && evt.photos.length > 0) {
    photoArea.innerHTML = evt.photos.map(p => `<img src="${p}" onclick="window.open('${p}', '_blank')" alt="Gallery Image">`).join('');
    document.getElementById('evtSectionPhotos').style.display = 'block';
  } else {
    document.getElementById('evtSectionPhotos').style.display = 'none';
  }

  document.getElementById('eventDetailModal').style.display = 'flex';
}

function closeEventDetail() {
  document.getElementById('eventDetailModal').style.display = 'none';
}

// Ensure DOM is ready, then load the home events
document.addEventListener('DOMContentLoaded', () => {
  renderEventCards(mockEvents.slice(0, 3), 'homeEventsGrid');
});
// --- END SUPER EVENT SYSTEM ---
'''
text = text.replace('// Hook into init', super_event_js + '\n// Hook into init')

# Add missing translations for the events section title
text = text.replace('"gallery.empty": "暂无公开相册。"', '"gallery.empty": "暂无公开相册。",\n    "events.title": "赛事与活动中心",\n    "events.sub": "记录百乐县中国象棋公会的精彩瞬间与赛事资源",\n    "events.view_all": "📚 查看所有历届活动 / View All Events"')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Super Event System implemented.")
