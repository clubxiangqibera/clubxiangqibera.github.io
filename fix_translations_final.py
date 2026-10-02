import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the English suffixes in the Chinese dictionary
text = text.replace('"nav.student_login": "学员专属登录 (Student Login)",', '"nav.student_login": "学员专属登录",')
text = text.replace('"nav.school_portal": "校际赛报名系统 (Schools)",', '"nav.school_portal": "校际赛报名系统",')
text = text.replace('"nav.admin_portal": "教练管理端 (Admin)",', '"nav.admin_portal": "教练管理端",')
text = text.replace('"nav.language": "系统语言 (Language)",', '"nav.language": "系统语言",')
text = text.replace('"nav.explore": "探索俱乐部 (Explore)",', '"nav.explore": "探索俱乐部",')
text = text.replace('"nav.portals": "专属入口 (Portals)",', '"nav.portals": "专属入口",')

# Just in case they are somewhere else
text = text.replace('学员专属登录 (Student Login)', '学员专属登录')
text = text.replace('校际赛报名系统 (Schools)', '校际赛报名系统')
text = text.replace('教练管理端 (Admin)', '教练管理端')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations fixed.")
