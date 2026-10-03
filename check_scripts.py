import io, sys
sys.stdout.reconfigure(encoding='utf-8')

for name in ['admin.html', 'school.html']:
    with io.open(name, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # check script tags
    scripts = text.split('<script>')
    print(name, 'has', len(scripts)-1, 'script blocks')
