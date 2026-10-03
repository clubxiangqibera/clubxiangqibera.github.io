import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# 1. Update index.html HTML defaults (remove emojis)
# ==========================================
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('🏠 首页', '首页')
text = text.replace('🏆 天梯榜', '天梯榜')
text = text.replace('📸 赛事与活动中心', '赛事与活动中心')
text = text.replace('🔐 学员专属登录', '学员专属登录')
text = text.replace('🏫 校际赛报名系统', '校际赛报名系统')
text = text.replace('👑 教练管理端', '教练管理端')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("index.html menu cleaned of emojis.")

# ==========================================
# 2. Update admin.html & school.html
# ==========================================
for file in ['admin.html', 'school.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean HTML of Mega Menu (remove all emojis, make all links #fff)
    content = content.replace('🏠 首页', '首页')
    content = content.replace('🏆 天梯榜', '天梯榜')
    content = content.replace('📸 赛事与活动中心', '赛事与活动中心')
    content = content.replace('🔐 学员专属登录', '学员专属登录')
    content = content.replace('🏫 校际赛报名系统', '校际赛报名系统')
    content = content.replace('👑 教练管理端', '教练管理端')
    content = content.replace('color:#F1C40F;', 'color:#fff;')

    # 2. Update JS in admin.html / school.html so language switches also don't insert emojis
    content = content.replace("'🏠 首页'", "'首页'")
    content = content.replace("'🏆 天梯榜'", "'天梯榜'")
    content = content.replace("'📸 赛事与活动中心'", "'赛事与活动中心'")
    content = content.replace("'🔐 学员专属登录'", "'学员专属登录'")
    content = content.replace("'🏫 校际赛报名系统'", "'校际赛报名系统'")
    content = content.replace("'👑 教练管理端'", "'教练管理端'")

    content = content.replace("'🏠 Utama'", "'Utama'")
    content = content.replace("'🏆 Kedudukan'", "'Kedudukan'")
    content = content.replace("'📸 Pusat Acara & Aktiviti'", "'Pusat Acara & Aktiviti'")
    content = content.replace("'🔐 Log Masuk Pelajar'", "'Log Masuk Pelajar'")
    content = content.replace("'🏫 Sistem Antara Sekolah'", "'Sistem Antara Sekolah'")
    content = content.replace("'👑 Portal Jurulatih'", "'Portal Jurulatih'")

    content = content.replace("'🏠 Home'", "'Home'")
    content = content.replace("'🏆 Ladder'", "'Ladder'")
    content = content.replace("'📸 Events & Activities'", "'Events & Activities'")
    content = content.replace("'🔐 Student Login'", "'Student Login'")
    content = content.replace("'🏫 Schools Portal'", "'Schools Portal'")
    content = content.replace("'👑 Admin Portal'", "'Admin Portal'")

    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{file} menu cleaned and synced!")

print("All 3 files synced to pure text menu matching Image 1!")
