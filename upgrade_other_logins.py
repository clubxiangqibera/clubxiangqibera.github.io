import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

css_animation = '''
@keyframes popZoom {
  0% { opacity: 0; transform: scale(0.9) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-zoom {
  animation: popZoom 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
'''

for filename in ['admin.html', 'school.html']:
    with io.open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Add css animation to styles
    if 'popZoom' not in text:
        text = text.replace('</style>', css_animation + '\n</style>')
    
    # 2. Add animate-zoom to login-card
    text = text.replace('class="login-card"', 'class="login-card animate-zoom"')
    
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

print("Admin and School UI upgraded with animations!")
