import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with io.open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the ticker wrap
ticker = re.search(r'<div class="ticker-wrap".*?</div>\s*</div>', text, flags=re.DOTALL)
if ticker:
    text = text.replace(ticker.group(0), '')

# 2. Update the footer text to remove redundancy
old_cn_desc = r'"footer.about_desc": "Club XiangQi Bera \(CXQB\)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。"'
new_cn_desc = r'"footer.about_desc": "彭亨百乐县唯一专业中国象棋教育学院，负责统筹全县赛事与等级分考级认证。"'
text = re.sub(old_cn_desc, new_cn_desc, text)

old_html_desc = r'<span data-i18n="footer.about_desc">Club XiangQi Bera \(CXQB\)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。</span>'
new_html_desc = r'<span data-i18n="footer.about_desc">彭亨百乐县唯一专业中国象棋教育学院，负责统筹全县赛事与等级分考级认证。</span>'
text = re.sub(old_html_desc, new_html_desc, text)

# Just in case, clean up any remaining old desc
text = text.replace('Club XiangQi Bera (CXQB)<br>彭亨百乐全县专业中国象棋培训、赛事与等级分考级体系认证机构。', '彭亨百乐县唯一专业中国象棋教育学院，负责统筹全县赛事与等级分考级认证。')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Ticker removed and Footer text updated.")
