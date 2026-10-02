import io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix: publicPodiumArea needs to be full-width, block-level
# The issue is likely that it's inside a flex/grid container that's making it share a row
# Let's find its container and add width:100%

# Add CSS fixes for the podium layout
css_fixes = '''
/* Ladder layout fixes */
#publicPodiumArea {
  width: 100%;
  display: block;
}
.podium {
  display: grid;
  grid-template-columns: 1fr 1.15fr 1fr;
  gap: 16px;
  align-items: end;
  width: 100%;
}
.rank-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
  text-align: center;
  background: var(--navy-900);
  border: 1px solid var(--line);
  border-radius: var(--radius);
}
.rank-card--1 {
  padding-block: 36px;
  border-color: var(--gold);
  background: linear-gradient(180deg, var(--navy-800), var(--navy-900));
}
.rank-card__no {
  width: 38px; height: 38px; margin-bottom: 12px;
  display: grid; place-items: center;
  font: 700 1rem var(--font-serif);
  color: var(--gold-soft);
  border: 1px solid var(--gold); border-radius: 50%;
}
.rank-card--1 .rank-card__no { background: var(--gold); color: var(--navy-950); }
.rank-card--2 .rank-card__no { border-color: var(--silver); color: var(--silver); }
.rank-card__name { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 700; }
.rank-card__school { margin-top: 2px; font-size: 0.82rem; color: var(--ink-dim); }
.rank-card__title {
  display: inline-block; margin-top: 12px; padding: 2px 12px;
  font-size: 0.78rem; color: var(--gold-soft);
  border: 1px solid var(--line); border-radius: var(--radius-pill);
}
.rank-card__rating {
  display: block; margin-top: 10px;
  font: 700 1.6rem var(--font-serif); color: var(--ink);
}

.rank-list {
  display: flex; flex-direction: column; gap: 12px; margin-top: 24px; width: 100%;
}
.rank-list-item {
  display: flex; align-items: center; gap: 16px; padding: 16px 20px;
  background: var(--navy-900); border: 1px solid var(--line); border-radius: var(--radius);
}
.rank-list-item__no { font: 700 1.1rem var(--font-serif); color: var(--gold-soft); width: 24px; text-align: center; flex-shrink: 0; }
.rank-list-item__info { flex: 1; }
.rank-list-item__name { font: 700 1.1rem var(--font-serif); color: var(--ink); }
.rank-list-item__school { display: block; font-size: 0.8rem; color: var(--ink-dim); }
.rank-list-item__rating { font: 700 1.25rem var(--font-serif); color: var(--gold); flex-shrink: 0; }

@media (max-width: 760px) {
  .podium { grid-template-columns: 1fr; }
  .rank-card--1 { order: -1; }
}
'''
text = text.replace('</style>', css_fixes + '\n</style>')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("CSS fixes applied.")
